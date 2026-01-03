"""
Handlers package
Barcha bot handlerlar uchun
"""

from handlers.start_hl import router as start_router
from handlers.workout_hi import workout_router
from handlers.exercises_hl import exercises_router
from handlers.progress_hi import progress_router
from handlers.nutrition_hi import nutrition_router
from handlers.help_hi import help_router

__all__ = [
    'start_router',
    'workout_router',
    'exercises_router',
    'progress_router',
    'nutrition_router',
    'help_router'
]