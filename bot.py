import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from config import TOKEN
from handlers.help_hi import help_router
from handlers.nutrition_hi import nutrition_router
from handlers.progress_hi import progress_router
from handlers.start_hl import router as start_router
from handlers.exercises_hl import exercises_router
from handlers.workout_hi import workout_router

load_dotenv()

# Dispatcher
dp = Dispatcher()


async def main() -> None:
    """
    Botni ishga tushirish
    """
    # Bot obyektini yaratish (proxy SHART EMAS!)
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Routerlarni tartib bilan qo'shish
    dp.include_router(start_router)
    dp.include_router(workout_router)
    dp.include_router(exercises_router)
    dp.include_router(progress_router)
    dp.include_router(nutrition_router)
    dp.include_router(help_router)

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
        import traceback

        traceback.print_exc()
        sys.exit(1)