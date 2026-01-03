"""
Keyboards package
Barcha keyboard layoutlar uchun
"""

from keyboards.inline_kbt import (
    get_exercises_keyboard,
    get_workout_plan_keyboard,
    get_workout_action_keyboard,
    get_meal_plan_keyboard,
    get_progress_menu_keyboard,
    get_weight_tracking_keyboard,
    get_nutrition_tips_keyboard
)

from keyboards.replay_kbt import (
    fitness_reply_menu,
    goals_keyboard
)

__all__ = [
    # Inline keyboards
    'get_exercises_keyboard',
    'get_workout_plan_keyboard',
    'get_workout_action_keyboard',
    'get_meal_plan_keyboard',
    'get_progress_menu_keyboard',
    'get_weight_tracking_keyboard',
    'get_nutrition_tips_keyboard',

    # Reply keyboards
    'fitness_reply_menu',
    'goals_keyboard'
]