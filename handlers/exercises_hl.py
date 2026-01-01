from aiogram import Router, F
from aiogram.types import CallbackQuery,Message
from keyboards.inline_kbt import get_exercises_keyboard
exercises_router = Router()


@exercises_router.message(lambda message: message.text == "🏋️ Exercises")
async def exercises_handler(message):
    await message.answer(
        "Qaysi turdagi mashqlarni ko‘rmoqchisiz?",
        reply_markup=get_exercises_keyboard()
    )


@exercises_router.callback_query(lambda callback: callback.data in ["home_workouts", "gym_workouts"])
async def show_exercises(callback: CallbackQuery):
    if callback.data == "home_workouts":
        exercises = ["Push-ups - 3x10", "Squats - 3x15", "Plank - 3 sets 30s"]
    else:
        exercises = ["Bench Press - 3x8", "Deadlift - 3x5", "Lat Pulldown - 3x10"]

    text = "\n".join(exercises)
    await callback.message.edit_text(f"🏋️ Tanlangan mashqlar:\n{text}")
    await callback.message.edit_reply_markup(reply_markup=None)


#
# @exercises_router.message(F.text == "/myprofile")
# async def show_profile(message: Message, state: FSMContext):
#     # User profilini olish uchun DB kerak bo‘lsa, F(get_db) bilan qo‘shish mumkin
#     await Message.answer("👤 Sizning profilingiz:")
