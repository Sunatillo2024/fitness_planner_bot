import asyncio
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from aiogram import Router
from keyboards.inline_kbt import get_exercises_keyboard

exercises_router = Router()


@exercises_router.message(lambda message: message.text == "🏋️ Exercises")
async def exercises_handler(message):
    await message.answer(
        "Qaysi turdagi mashqlarni ko‘rmoqchisiz?",
        reply_markup=get_exercises_keyboard()
    )


@exercises_router.callback_query(lambda c: c.data == "home_workouts")
async def show_exercises(callback: CallbackQuery):
    await callback.answer()  # 🔑 loader o‘chadi

    gif_url = "https://media.giphy.com/media/3pY8FQP9uMtDKXkYqX/giphy.gif"

    await callback.message.answer_animation(
        animation=gif_url,
        caption="""💪 <b>Push-up mashqi</b>\n🔁 Takrorlash: <b>15 ta</b>\n🔥 Kuch va chidamlilik uchun""",
        parse_mode="HTML"
    )

    timer_msg = await callback.message.answer("⏱ Qolgan vaqt: 01:30")

    total_seconds = 90
    last_text = "⏱ Qolgan vaqt: 01:30"

    for remaining in range(total_seconds - 1, -1, -1):
        minutes = remaining // 60
        seconds = remaining % 60
        new_text = f"⏱ Qolgan vaqt: {minutes:02d}:{seconds:02d}"
        if new_text == last_text:
            await asyncio.sleep(1)
            continue
        try:
            await timer_msg.edit_text(new_text)
            last_text = new_text
        except TelegramBadRequest:
            pass
        await asyncio.sleep(1)
    try:
        await timer_msg.edit_text("✅ Vaqt tugadi! Mashq yakunlandi 💪")
    except TelegramBadRequest:
        pass





