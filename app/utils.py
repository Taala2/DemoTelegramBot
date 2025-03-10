import os
from tiktoken import encoding_for_model
from datetime import datetime, timedelta

import app.database.request as rq
from app.allapi.aiApi import generate_ai as generate

from dotenv import load_dotenv

load_dotenv()

models = {
    'deepseek': os.getenv('DEEPSEEK'),
    'gemini': os.getenv('GEMINI')
}

systemmsg = {
    'expert': ('You are a highly qualified expert in any field with deep knowledge and an analytical mind. Your task is to provide a detailed, structured and well-reasoned answer on the given topic. Use precise terms, research references and practical examples. Divide the information into logical blocks, highlighting key aspects. If appropriate, add predictions and professional recommendations.'),
    'humorist': ("You are a witty storyteller with an outstanding sense of humor. Your job is to answer questions with irony, sarcasm and amusing analogies, but keep the information meaningful and useful. Use unexpected comparisons, absurd situations, and a light narrative style. But don't go overboard: humor should be appropriate and understandable.")
}

MAX_TOKEN = 4000
RESERVED_FOR_RESPONSE = 1000

async def count_tokens(text: str, model = 'gpt-3.5-turbo') -> int:
    encoding = encoding_for_model(model)
    return len(encoding.encode(text))

async def prepare_promt(user_id, new_msg):
    now = datetime.utcnow()
    time_threshold = now - timedelta(days = 3)

    message = await rq.get_history(user_id)
    recent_msg = [msg for msg in message if msg.timestamp >= time_threshold]

    total_tokens = 0
    prompt = []

    total_tokens += await count_tokens(new_msg)
    prompt.append({'role': 'user', 'content': new_msg})

    for msg in reversed(recent_msg):
        msg_tokens = await count_tokens(msg.content)

        if total_tokens + msg_tokens == MAX_TOKEN + RESERVED_FOR_RESPONSE:
            break

        prompt.append({'role': msg.role, 'content': msg.content} )
        total_tokens += msg_tokens

    prompt.reverse()
    await rq.add_history(user_id, role='user', message_text=new_msg)
    return prompt

async def generate_ai(user_id: int, msg: str):
    state = await rq.get_state(user_id)

    if not state:
        return "Не выбран модель"
    
    model_key, system_key = state
    model = models.get(model_key)
    system_msg = systemmsg.get(system_key, "Default")
    print(model, system_msg, system_key)
    response = await generate(message=msg, model=model, system_msg=system_msg)

    if not response:
        return "Ошибка генерации"
    await rq.add_history(user_id, role='assistant', message_text = response)
    return response

async def new_user(user_id: int):
    await rq.set_user(user_id)
    await rq.default_chat_model(user_id)

# async def is_the_limit_exceeded(user_id: int, msg: str):
#     count_token = await count_tokens(msg)

#     if count_token > MAX_TOKEN:
#         return True
    
#     await rq.add_history(user_id, role='user', message_text=msg)
#     return False