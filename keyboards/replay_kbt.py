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


goals_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Weight Loss")],
        [KeyboardButton(text="Muscle Gain")],
        [KeyboardButton(text="Healthy Life")]
    ],
    resize_keyboard=True
)