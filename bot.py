import asyncio
import logging
import socket
import sys

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from config import TOKEN
from handlers.help_hi import help_router
from handlers.nutrition_hi import nutrition_router
from handlers.progress_hi import progress_router

# Handlers
from handlers.start_hl import router as start_router
from handlers.exercises_hl import exercises_router
from handlers.workout_hi import workout_router

load_dotenv()

# Dispatcher
dp = Dispatcher()


async def main() -> None:
    """Bot ishga tushirish"""
    connector = aiohttp.TCPConnector(family=socket.AF_INET)
    session = aiohttp.ClientSession(connector=connector)

    bot = Bot(
        token=TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


    # Routerlarni tartib bilan qo'shish
    dp.include_router(start_router)  # /start va registration
    dp.include_router(workout_router)  # 💪 Workout Plans
    dp.include_router(exercises_router)  # 🏋️ Exercises
    dp.include_router(progress_router)  # 📊 My Progress
    dp.include_router(nutrition_router)  # 🥗 Nutrition + 🍎 Meal Plan
    dp.include_router(help_router)  # ❓ Help

    # Botni polling rejimida ishga tushirish
    print("✅ Bot polling rejimida ishlayapti...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Logging sozlamalari
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=" * 50)
    print("🤖 Fitness Planner Bot ishga tushmoqda...")
    print("=" * 50)

    # Database jadvallarini yaratish
    print("📊 Database jadvallarini yaratish...")
    from database.db import Base, engine

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database jadvallar muvaffaqiyatli yaratildi!")
    except Exception as e:
        print(f"❌ Database xatolik: {e}")
        sys.exit(1)

    print("=" * 50)
    print("🚀 Bot ishga tushdi!")
    print("💪 Fitness Planner Bot faol...")
    print("=" * 50)

    # Botni ishga tushirish
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("⏹ Bot to'xtatildi (Ctrl+C)")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Xatolik yuz berdi: {e}")
        sys.exit(1)