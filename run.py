import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from app.handler import router
from app.database.models import init_db

from dotenv import load_dotenv

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dispatcher = Dispatcher()
    await init_db()
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")