from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def fitness_reply_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="💪 Workout Plans"), KeyboardButton(text="🏋️ Exercises")],
        [KeyboardButton(text="🥗 Nutrition Tips"), KeyboardButton(text="🍎 Meal Plan")],
        [KeyboardButton(text="📊 My Progress"), KeyboardButton(text="❓ Help")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

