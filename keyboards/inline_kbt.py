from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_exercises_keyboard() -> InlineKeyboardMarkup:
    """
    🏋️ Exercises tugmasi uchun inline keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Home Workouts", callback_data="home_workouts")],
            [InlineKeyboardButton(text="🏋️ Gym Workouts", callback_data="gym_workouts")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ]
    )
    return keyboard


def get_workout_plan_keyboard() -> InlineKeyboardMarkup:
    """
    💪 Workout Plans uchun keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Home Workout", callback_data="workout_home")],
            [InlineKeyboardButton(text="🏋️ Gym Workout", callback_data="workout_gym")],
        ]
    )
    return keyboard


def get_workout_action_keyboard() -> InlineKeyboardMarkup:
    """
    Mashq jarayonida ishlatiladigan keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶️ Timer Boshlash", callback_data="start_timer")],
            [
                InlineKeyboardButton(text="⏸ Dam Olish", callback_data="rest_pause"),
                InlineKeyboardButton(text="➡️ Keyingisi", callback_data="next_exercise")
            ],
            [InlineKeyboardButton(text="✅ Tugatish", callback_data="finish_workout")]
        ]
    )
    return keyboard


def get_meal_plan_keyboard() -> InlineKeyboardMarkup:
    """
    🍎 Meal Plan uchun keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍽 Muvozanatli Reja", callback_data="meal_balanced")],
            [InlineKeyboardButton(text="📉 Vazn Tashlash", callback_data="meal_weight_loss")],
            [InlineKeyboardButton(text="💪 Mushak Oshirish", callback_data="meal_muscle_gain")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ]
    )
    return keyboard


def get_progress_menu_keyboard() -> InlineKeyboardMarkup:
    """
    📊 Progress menu keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏋️ Workout Statistika", callback_data="progress_workout")],
            [InlineKeyboardButton(text="⚖️ Vazn Tarixingiz", callback_data="progress_weight")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ]
    )
    return keyboard


def get_weight_tracking_keyboard() -> InlineKeyboardMarkup:
    """
    ⚖️ Weight tracking keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Vazn Qo'shish", callback_data="add_weight")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="progress_back")]
        ]
    )
    return keyboard


def get_nutrition_tips_keyboard() -> InlineKeyboardMarkup:
    """
    🥗 Nutrition tips keyboard
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Yana Maslahat", callback_data="nutrition_tip")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")]
        ]
    )
    return keyboard