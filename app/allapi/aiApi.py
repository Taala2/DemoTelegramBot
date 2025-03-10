import os
from openai import AsyncOpenAI
import logging

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('AI_TOKEN'),
)


async def generate_ai(message: str, model):
    try:
        completion = await client.chat.completions.create(
        model = model,
        messages = message
        )
        print(completion)
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Ошибка в AI: {e}")
        return "Ошибка генерации ответа, попробуйте позже."
