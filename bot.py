import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from config import TOKEN
from handlers.exercises_hl import exercises_router
from handlers.start_hl import router

load_dotenv()

dp = Dispatcher(bot=Bot(TOKEN))



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router)
    dp.include_router(exercises_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("Creating tables...")
    from database.db import Base, engine

    Base.metadata.create_all(bind=engine)
    asyncio.run(main())
