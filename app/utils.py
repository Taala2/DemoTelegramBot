import os
import logging
from dotenv import load_dotenv

from tiktoken import encoding_for_model
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

import app.database.request as rq
from app.allapi.aiApi import generate_ai as generate
from app.constants import Messages

load_dotenv()

models = {"deepseek": os.getenv("DEEPSEEK"), "gemini": os.getenv("GEMINI")}

if not all(models.values()):
    raise ValueError("Missing model tokens in environment variables")

systemmsg = {
    "expert": (
        "You are a highly qualified expert in any field with deep knowledge and an analytical mind. Your task is to provide a detailed, structured and well-reasoned answer on the given topic. Use precise terms, research references and practical examples. Divide the information into logical blocks, highlighting key aspects. If appropriate, add predictions and professional recommendations."
    ),
    "humorist": (
        "You are a witty storyteller with an outstanding sense of humor. Your job is to answer questions with irony, sarcasm and amusing analogies, but keep the information meaningful and useful. Use unexpected comparisons, absurd situations, and a light narrative style. But don't go overboard: humor should be appropriate and understandable."
    ),
}

MAX_TOKEN = 4000
RESERVED_FOR_RESPONSE = 1000
MAX_REQUESTS_PER_DAY = 50

request_counts: Dict[int, Tuple[int, datetime]] = {}


async def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    try:
        encoding = encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        logging.error(f"Error counting tokens: {e}")
        return 0


async def check_rate_limit(tg_id: int) -> bool:
    """Check if user has exceeded their daily request limit"""
    now = datetime.utcnow()
    if tg_id in request_counts:
        count, last_reset = request_counts[tg_id]
        if now - last_reset >= timedelta(days=1):
            request_counts[tg_id] = (1, now)
            return True
        if count >= MAX_REQUESTS_PER_DAY:
            return False
        request_counts[tg_id] = (count + 1, last_reset)
    else:
        request_counts[tg_id] = (1, now)
    return True


async def prepare_promt(tg_id: int, new_msg: str) -> List[Dict[str, str]]:
    """
    Prepare prompt for AI model
    
    :param tg_id: Telegram user ID
    :param new_msg: User message
    """

    try:
        if not await check_rate_limit(tg_id):
            logging.warning(f"User {tg_id} exceeded daily request limit")
            raise ValueError("Daily request limit exceeded")

        now = datetime.utcnow()
        time_threshold = now - timedelta(days=3)

        message = await rq.get_history(tg_id)
        recent_msg = [msg for msg in message if msg.timestamp >= time_threshold]

        total_tokens = 0
        prompt = []

        total_tokens += await count_tokens(new_msg)
        prompt.append({"role": "user", "content": new_msg})

        for msg in reversed(recent_msg):
            msg_tokens = await count_tokens(msg.content)

            if total_tokens + msg_tokens >= MAX_TOKEN - RESERVED_FOR_RESPONSE:
                break

            prompt.append({"role": msg.role, "content": msg.content})
            total_tokens += msg_tokens

        prompt.reverse()
        await rq.add_history(tg_id, role="user", message_text=new_msg)
        return prompt

    except ValueError as e:
        logging.error(f"Error in prepare_prompt for user {tg_id}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in prepare_prompt: {e}")
        raise


async def generate_ai(tg_id: int, msg: str) -> str:
    """
    Generate response from AI model
    
    :param tg_id: Telegram user ID
    :param msg: User message
    """

    try:
        state = await rq.get_state(tg_id)

        if not state:
            return "Model not selected"

        model_key, system_key = state
        model = models.get(model_key)
        system_msg = systemmsg.get(system_key, "Default")

        logging.info(f"Generating response for user {tg_id} with model {model_key}")
        response = await generate(message=msg, model=model, system_msg=system_msg)

        if not response:
            return Messages.ERROR_GENERATION

        await rq.add_history(tg_id, role="assistant", message_text=response)
        return response

    except Exception as e:
        logging.error(f"Error in generate_ai for user {tg_id}: {e}")
        return Messages.ERROR_GENERATION


async def new_user(tg_id: int) -> None:
    """
    Initialize new user in the database
    tg_id: Telegram user ID
    """
    try:
        await rq.set_user(tg_id)
        await rq.default_chat_model(tg_id)
        logging.info(f"New user initialized: {tg_id}")
    except Exception as e:
        logging.error(f"Error initializing new user {tg_id}: {e}")
        raise
