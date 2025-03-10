import os
from openai import AsyncOpenAI, APIError, RateLimitError
import logging
from typing import Union, List, Dict

from dotenv import load_dotenv
from app.constants import Messages

load_dotenv()
logging.basicConfig(level=logging.INFO)

AI_TOKEN = os.getenv('AI_TOKEN')
if not AI_TOKEN:
    raise ValueError("AI_TOKEN environment variable is not set")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)

async def generate_ai(message: Union[str, List[Dict[str, str]]], model: str, system_msg: str = 'Default') -> str:
    if not model:
        logging.error("Model parameter is empty")
        return Messages.ERROR_GENERATION

    if not isinstance(message, list):
        message = [{"role": "user", "content": message}]
    
    full_msg = [{"role": "system", "content": system_msg}] + message
    
    try:
        completion = await client.chat.completions.create(
            model=model,
            messages=full_msg,
        )
        logging.info(f'Response received from AI: {completion.choices[0].message.content}')
        return completion.choices[0].message.content
    except RateLimitError as e:
        logging.error(f"Rate limit exceeded: {e}")
        return "Rate limit exceeded. Please try again later."
    except APIError as e:
        logging.error(f"API Error: {e}")
        return Messages.ERROR_GENERATION
    except Exception as e:
        logging.error(f"Unexpected error in generate_ai: {e}")
        return Messages.ERROR_GENERATION
