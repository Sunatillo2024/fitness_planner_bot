from aiogram.fsm.state import StatesGroup, State


class UserInfo(StatesGroup):
    name = State()
    age = State()
    weight = State()
    height = State()
    goal = State()


class WorkoutSession(StatesGroup):
    in_progress = State()