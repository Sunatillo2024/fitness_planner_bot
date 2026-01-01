from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_exercises_keyboard() -> InlineKeyboardMarkup:
    """
    🏋️ Exercises tugmasi uchun inline keyboard yaratadi.
    - Home Workouts
    - Gym Workouts
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Home Workouts", callback_data="home_workouts")],
            [InlineKeyboardButton(text="🏋️ Gym Workouts", callback_data="gym_workouts")]
        ]
    )
    return keyboard
