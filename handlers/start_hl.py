from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram import html

from keyboards.replay_kbt import fitness_reply_menu

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    gif_url = "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif"
    caption = (
        "👋 Assalomu alaykum!\n"
        "🏋️‍♂️ Fitness Planner Bot ga xush kelibsiz!\n"
        "✨ Bu yerda siz mashg‘ulotlaringizni rejalashtirasiz va natijalaringizni kuzatib borasiz."
    )

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=fitness_reply_menu())
    await message.answer_animation(
        animation=gif_url,  # 🔑 MUHIM — bu argument berilishi kerak
        caption=caption
    )


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


@router.message(F.text == "💪 Workout Plans")
async def workout_handler(message: Message):
    await message.answer("💪 Workout rejalarini tanlang: Beginner / Intermediate / Advanced")


@router.message(F.text == "🥗 Nutrition Tips")
async def nutrition_handler(message: Message):
    await message.answer("🥗 Kunlik ovqatlanish bo‘yicha maslahatlar!")
