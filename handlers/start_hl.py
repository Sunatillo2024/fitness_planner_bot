from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import html

from States.user_state import UserInfo
from keyboards.replay_kbt import fitness_reply_menu, goals_keyboard

router = Router()


# ---------- START COMMAND ----------
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    print(message.text)
    from database.db import SessionLocal
    from database.models import User

    telegram_id = message.from_user.id

    # DB session ochamiz
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
    finally:
        db.close()

    if user:
        # ⚡ Foydalanuvchi allaqachon bor — FSM ishlamaydi
        await message.answer(
            f"Salom, {html.bold(message.from_user.full_name)}! Boshladik bolmasam .",
            reply_markup=fitness_reply_menu()
        )
        return  # handler shu yerda tugaydi

    # ⚡ Yangi foydalanuvchi — FSM ishga tushadi
    gif_url = "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif"
    caption = (
        "👋 Assalomu alaykum!\n"
        "🏋️‍♂️ Fitness Planner Bot ga xush kelibsiz!\n"
        "✨ Bu yerda siz mashg‘ulotlaringizni rejalashtirasiz va natijalaringizni kuzatib borasiz."
    )

    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=fitness_reply_menu()
    )
    await message.answer_animation(animation=gif_url, caption=caption)
    await message.answer("Avvalo, ismingizni kiriting:")

    await state.set_state(UserInfo.name)



# ---------- 1️⃣ NAME ----------
@router.message(StateFilter(UserInfo.name))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(UserInfo.age)



# ---------- 2️⃣ AGE ----------
@router.message(StateFilter(UserInfo.age))
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Iltimos, raqam formatida kiriting (masalan: 20)")
        return
    await state.update_data(age=age)
    await message.answer("Vazningizni kiriting (kg):")
    await state.set_state(UserInfo.weight)


# ---------- 3️⃣ WEIGHT ----------
@router.message(StateFilter(UserInfo.weight))
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
    except ValueError:
        await message.answer("Iltimos, raqam formatida kiriting (masalan: 70.5)")
        return
    await state.update_data(weight=weight)
    await message.answer("Bo‘yingizni kiriting (cm):")
    await state.set_state(UserInfo.height)


# ---------- 4️⃣ HEIGHT ----------
@router.message(StateFilter(UserInfo.height))
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
    except ValueError:
        await message.answer("Iltimos, raqam formatida kiriting (masalan: 175)")
        return
    await state.update_data(height=height)
    await message.answer("Maqsadingizni tanlang:", reply_markup=goals_keyboard)
    await state.set_state(UserInfo.goal)


# ---------- 5️⃣ GOAL + DB SAVE ----------
from database.db import SessionLocal
from database.session import create_user  # yuqoridagi funksiya joylashgan fayl


@router.message(StateFilter(UserInfo.goal))
async def process_goal(message: Message, state: FSMContext):
    user_data = await state.get_data()
    telegram_id = message.from_user.id
    goal_map = {
        "Weight Loss": "weight_loss",
        "Muscle Gain": "muscle_gain",
        "Healthy Life": "healthy_life"
    }
    selected_goal = goal_map.get(message.text, "healthy_life")

    # DB session ochish
    db = SessionLocal()
    try:
        create_user(db, telegram_id, user_data, selected_goal)
    finally:
        db.close()

    await message.answer(
        "Profilingiz saqlandi! Endi 💪 /workout bilan mashq olishingiz mumkin.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
