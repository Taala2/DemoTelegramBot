import os
from tiktoken import encoding_for_model
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional, Tuple

import app.database.request as rq
from app.allapi.aiApi import generate_ai as generate
from app.constants import Messages

from dotenv import load_dotenv

load_dotenv()

models = {
    'deepseek': os.getenv('DEEPSEEK'),
    'gemini': os.getenv('GEMINI')
}

if not all(models.values()):
    raise ValueError("Missing model tokens in environment variables")

systemmsg = {
    'expert': ('You are a highly qualified expert in any field with deep knowledge and an analytical mind. Your task is to provide a detailed, structured and well-reasoned answer on the given topic. Use precise terms, research references and practical examples. Divide the information into logical blocks, highlighting key aspects. If appropriate, add predictions and professional recommendations.'),
    'humorist': ("You are a witty storyteller with an outstanding sense of humor. Your job is to answer questions with irony, sarcasm and amusing analogies, but keep the information meaningful and useful. Use unexpected comparisons, absurd situations, and a light narrative style. But don't go overboard: humor should be appropriate and understandable.")
}

MAX_TOKEN = 4000
RESERVED_FOR_RESPONSE = 1000
MAX_REQUESTS_PER_DAY = 50

request_counts: Dict[int, Tuple[int, datetime]] = {}

async def count_tokens(text: str, model: str = 'gpt-3.5-turbo') -> int:
    try:
        encoding = encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        logging.error(f"Error counting tokens: {e}")
        return 0

async def check_rate_limit(user_id: int) -> bool:
    """Check if user has exceeded their daily request limit"""
    now = datetime.utcnow()
    if user_id in request_counts:
        count, last_reset = request_counts[user_id]
        if now - last_reset >= timedelta(days=1):
            request_counts[user_id] = (1, now)
            return True
        if count >= MAX_REQUESTS_PER_DAY:
            return False
        request_counts[user_id] = (count + 1, last_reset)
    else:
        request_counts[user_id] = (1, now)
    return True

async def prepare_promt(user_id: int, new_msg: str) -> List[Dict[str, str]]:
    try:
        if not await check_rate_limit(user_id):
            logging.warning(f"User {user_id} exceeded daily request limit")
            raise ValueError("Daily request limit exceeded")

        now = datetime.utcnow()
        time_threshold = now - timedelta(days=3)

        message = await rq.get_history(user_id)
        recent_msg = [msg for msg in message if msg.timestamp >= time_threshold]

        total_tokens = 0
        prompt = []

        total_tokens += await count_tokens(new_msg)
        prompt.append({'role': 'user', 'content': new_msg})

        for msg in reversed(recent_msg):
            msg_tokens = await count_tokens(msg.content)

            if total_tokens + msg_tokens >= MAX_TOKEN - RESERVED_FOR_RESPONSE:
                break

            prompt.append({'role': msg.role, 'content': msg.content})
            total_tokens += msg_tokens

        prompt.reverse()
        await rq.add_history(user_id, role='user', message_text=new_msg)
        return prompt

    except ValueError as e:
        logging.error(f"Error in prepare_prompt for user {user_id}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in prepare_prompt: {e}")
        raise

async def generate_ai(user_id: int, msg: str) -> str:
    try:
        state = await rq.get_state(user_id)

        if not state:
            return "Model not selected"
        
        model_key, system_key = state
        model = models.get(model_key)
        system_msg = systemmsg.get(system_key, "Default")
        
        logging.info(f"Generating response for user {user_id} with model {model_key}")
        response = await generate(message=msg, model=model, system_msg=system_msg)

        if not response:
            return Messages.ERROR_GENERATION
            
        await rq.add_history(user_id, role='assistant', message_text=response)
        return response

    except Exception as e:
        logging.error(f"Error in generate_ai for user {user_id}: {e}")
        return Messages.ERROR_GENERATION

async def new_user(user_id: int) -> None:
    try:
        await rq.set_user(user_id)
        await rq.default_chat_model(user_id)
        logging.info(f"New user initialized: {user_id}")
    except Exception as e:
        logging.error(f"Error initializing new user {user_id}: {e}")
        raise

# async def is_the_limit_exceeded(user_id: int, msg: str):
#     count_token = await count_tokens(msg)

#     if count_token > MAX_TOKEN:
#         return True
    
#     await rq.add_history(user_id, role='user', message_text=msg)
#     return False