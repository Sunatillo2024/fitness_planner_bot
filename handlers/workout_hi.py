from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.inline_kbt import get_workout_plan_keyboard, get_workout_action_keyboard
from database.db import SessionLocal
from database.crud import (
    create_workout_session,
    complete_workout_session,
    add_exercise_log
)
import asyncio

workout_router = Router()


class WorkoutState(StatesGroup):
    in_session = State()


# Mashqlar ma'lumotlari
HOME_WORKOUTS = [
    {
        "name": "Push-ups",
        "gif": "https://media.giphy.com/media/ZeAXZfK2v3z6hmMZEj/giphy.gif",
        "sets_reps": "3 sets × 10 reps",
        "duration": 60,
        "description": "💪 Ko'krak va qo'llarni kuchaytiradi\n🎯 Triceps, chest, shoulders"
    },
    {
        "name": "Squats",
        "gif": "https://media.giphy.com/media/1qfDU4MJv9xoGtRKvh/giphy.gif",
        "sets_reps": "3 sets × 15 reps",
        "duration": 60,
        "description": "🦵 Oyoqlar va dumba mushaklari\n🎯 Quads, glutes, hamstrings"
    },
    {
        "name": "Sit-ups",
        "gif": "https://media.giphy.com/media/2A75RyXVzzSI2bx4Gj/giphy.gif",
        "sets_reps": "3 sets × 12 reps",
        "duration": 60,
        "description": "🔥 Qorin mushaklarini mustahkamlash\n🎯 Abs, core stability"
    },
    {
        "name": "Plank Hold",
        "gif": "https://media.giphy.com/media/3o7TKPATxjbMM6l8Mo/giphy.gif",
        "sets_reps": "3 sets × 30 sec",
        "duration": 90,
        "description": "⚡ Core kuchi va barqarorlik\n🎯 Full core, shoulders"
    },
    {
        "name": "Jumping Jacks",
        "gif": "https://media.giphy.com/media/26u4b45b8KlgAB7iM/giphy.gif",
        "sets_reps": "3 sets × 20 reps",
        "duration": 60,
        "description": "❤️ Kardio va endurance\n🎯 Full body cardio"
    }
]

GYM_WORKOUTS = [
    {
        "name": "Bench Press",
        "gif": "https://media.giphy.com/media/3oEdva0KggGvBqB7Fe/giphy.gif",
        "sets_reps": "4 sets × 8 reps",
        "duration": 90,
        "description": "💪 Ko'krak mushaklari\n🎯 Chest, triceps, shoulders"
    },
    {
        "name": "Deadlift",
        "gif": "https://media.giphy.com/media/3oEjI5VtIhHvK37WYo/giphy.gif",
        "sets_reps": "4 sets × 5 reps",
        "duration": 90,
        "description": "🔥 Orqa va oyoq kuchi\n🎯 Back, legs, core"
    },
    {
        "name": "Lat Pulldown",
        "gif": "https://media.giphy.com/media/26u4cqiYI30juCOGY/giphy.gif",
        "sets_reps": "3 sets × 10 reps",
        "duration": 75,
        "description": "💪 Orqa mushaklar kengligi\n🎯 Lats, biceps"
    },
    {
        "name": "Shoulder Press",
        "gif": "https://media.giphy.com/media/xT8qBbx0BXs6oc0lgs/giphy.gif",
        "sets_reps": "3 sets × 8 reps",
        "duration": 75,
        "description": "⚡ Yelka kuchi\n🎯 Shoulders, triceps"
    },
    {
        "name": "Barbell Rows",
        "gif": "https://media.giphy.com/media/3oKIPlifLxdhyETJRK/giphy.gif",
        "sets_reps": "3 sets × 10 reps",
        "duration": 75,
        "description": "💪 Orqa qalinligi\n🎯 Back thickness, biceps"
    }
]


@workout_router.message(F.text == "💪 Workout Plans")
async def workout_plans_menu(message: Message):
    """Workout turini tanlash menyu"""
    await message.answer(
        "🏋️‍♂️ <b>Workout turini tanlang:</b>\n\n"
        "🏠 <b>Home Workout</b>\n"
        "   • Hech qanday asbob kerak emas\n"
        "   • 5 ta asosiy mashq\n"
        "   • ~20-25 daqiqa\n\n"
        "🏋️ <b>Gym Workout</b>\n"
        "   • Zal uskunalari bilan\n"
        "   • 5 ta professional mashq\n"
        "   • ~30-35 daqiqa",
        reply_markup=get_workout_plan_keyboard()
    )


@workout_router.callback_query(F.data.in_(["workout_home", "workout_gym"]))
async def start_workout(callback: CallbackQuery, state: FSMContext):
    """Workout sessionni boshlash"""
    workout_type = "home" if callback.data == "workout_home" else "gym"
    exercises = HOME_WORKOUTS if workout_type == "home" else GYM_WORKOUTS

    # DB ga yangi session yaratamiz
    db = SessionLocal()
    try:
        session = create_workout_session(
            db=db,
            telegram_id=callback.from_user.id,
            workout_type=workout_type,
            total_exercises=len(exercises)
        )
        session_id = session.id
    finally:
        db.close()

    # FSM state'ga ma'lumotlarni saqlaymiz
    await state.update_data(
        session_id=session_id,
        workout_type=workout_type,
        exercises=exercises,
        current_index=0,
        completed_count=0,
        start_time=asyncio.get_event_loop().time()
    )

    await callback.message.edit_text(
        f"✅ <b>{'🏠 Home' if workout_type == 'home' else '🏋️ Gym'} Workout boshlandi!</b>\n\n"
        f"📊 Jami mashqlar: <b>{len(exercises)}</b> ta\n"
        f"⏱ Taxminiy vaqt: <b>{sum(e['duration'] for e in exercises) // 60}</b> daqiqa\n\n"
        f"💡 Har bir mashq uchun:\n"
        f"   • GIF animatsiya ko'rsatiladi\n"
        f"   • Timer ishga tushadi\n"
        f"   • Dam olish mumkin\n\n"
        f"🎯 Tayyor bo'lsangiz, boshlang!"
    )

    await state.set_state(WorkoutState.in_session)
    await asyncio.sleep(2)
    await show_exercise(callback.message, state)


async def show_exercise(message: Message, state: FSMContext):
    """Joriy mashqni ko'rsatish"""
    data = await state.get_data()
    exercises = data["exercises"]
    current_index = data["current_index"]

    if current_index >= len(exercises):
        await finish_workout(message, state)
        return

    exercise = exercises[current_index]
    progress = f"{current_index + 1}/{len(exercises)}"

    caption = (
        f"🏋️‍♂️ <b>Mashq {progress}</b>\n\n"
        f"<b>{exercise['name']}</b>\n\n"
        f"{exercise['description']}\n\n"
        f"📊 <b>Hajm:</b> {exercise['sets_reps']}\n"
        f"⏱ <b>Vaqt:</b> {exercise['duration']} soniya\n\n"
        f"💡 Tayyor bo'lsangiz timer boshlang!"
    )

    await message.answer_animation(
        animation=exercise["gif"],
        caption=caption,
        reply_markup=get_workout_action_keyboard()
    )


@workout_router.callback_query(F.data == "start_timer", WorkoutState.in_session)
async def start_timer(callback: CallbackQuery, state: FSMContext):
    """Timer ni boshlash"""
    data = await state.get_data()
    exercises = data["exercises"]
    current_index = data["current_index"]
    exercise = exercises[current_index]
    duration = exercise["duration"]

    await callback.answer("⏱ Timer boshlandi!")

    # Timer animatsiyasi
    for remaining in range(duration, 0, -5):  # Har 5 soniyada yangilanadi
        if remaining <= 10:  # Oxirgi 10 soniya har soniya
            for sec in range(min(remaining, 5), 0, -1):
                try:
                    await callback.message.edit_caption(
                        caption=f"⏱ <b>Qolgan vaqt: {sec} soniya</b>\n\n"
                                f"💪 <b>{exercise['name']}</b>\n"
                                f"📊 {exercise['sets_reps']}\n\n"
                                f"{'🔥' * (11 - sec)} {'⚪' * (sec - 1)}"
                    )
                    await asyncio.sleep(1)
                except Exception:
                    break
            break
        else:
            try:
                progress_bars = int((duration - remaining) / duration * 10)
                await callback.message.edit_caption(
                    caption=f"⏱ <b>Qolgan vaqt: {remaining} soniya</b>\n\n"
                            f"💪 <b>{exercise['name']}</b>\n"
                            f"📊 {exercise['sets_reps']}\n\n"
                            f"{'🔥' * progress_bars}{'⚪' * (10 - progress_bars)}"
                )
                await asyncio.sleep(5)
            except Exception:
                break

    # Timer tugadi
    await callback.message.edit_caption(
        caption=f"✅ <b>{exercise['name']} tugadi!</b>\n\n"
                f"🎉 Ajoyib bajarildi!\n"
                f"💪 {exercise['sets_reps']}\n\n"
                f"Keyingisiga o'tishingiz yoki dam olishingiz mumkin.",
        reply_markup=get_workout_action_keyboard()
    )


@workout_router.callback_query(F.data == "next_exercise", WorkoutState.in_session)
async def next_exercise(callback: CallbackQuery, state: FSMContext):
    """Keyingi mashqga o'tish"""
    data = await state.get_data()
    current_index = data["current_index"]
    exercises = data["exercises"]
    session_id = data["session_id"]

    # Hozirgi mashqni DB ga loglaymiz
    exercise = exercises[current_index]
    db = SessionLocal()
    try:
        add_exercise_log(
            db=db,
            session_id=session_id,
            exercise_name=exercise["name"],
            sets_reps=exercise["sets_reps"],
            duration=exercise["duration"]
        )
    finally:
        db.close()

    # State'ni yangilaymiz
    await state.update_data(
        current_index=current_index + 1,
        completed_count=data.get("completed_count", 0) + 1
    )

    await callback.message.delete()
    await show_exercise(callback.message, state)


@workout_router.callback_query(F.data == "rest_pause", WorkoutState.in_session)
async def rest_pause(callback: CallbackQuery):
    """Dam olish"""
    rest_time = 30

    await callback.answer(f"⏸ {rest_time} soniya dam oling!")

    msg = await callback.message.answer(
        f"⏸ <b>Dam olish vaqti</b>\n\n"
        f"🧘‍♂️ {rest_time} soniya dam oling\n"
        f"💧 Suv iching\n"
        f"🫁 Chuqur nafas oling"
    )

    for i in range(rest_time, 0, -5):
        await asyncio.sleep(5)
        if i > 5:
            await msg.edit_text(
                f"⏸ <b>Dam olish vaqti</b>\n\n"
                f"⏱ Qolgan: {i - 5} soniya\n"
                f"💧 Suv iching\n"
                f"🫁 Chuqur nafas oling"
            )

    await msg.edit_text("✅ <b>Dam olish tugadi!</b>\n\n💪 Davom etishingiz mumkin!")
    await asyncio.sleep(2)
    await msg.delete()


@workout_router.callback_query(F.data == "finish_workout", WorkoutState.in_session)
async def finish_workout_handler(callback: CallbackQuery, state: FSMContext):
    """Workout ni tugatish"""
    await callback.message.delete()
    await finish_workout(callback.message, state)


async def finish_workout(message: Message, state: FSMContext):
    """Workout sessionni yakunlash"""
    data = await state.get_data()
    session_id = data["session_id"]
    start_time = data["start_time"]
    completed_count = data.get("completed_count", 0)
    total_exercises = len(data["exercises"])

    total_duration = int(asyncio.get_event_loop().time() - start_time)

    # DB ga yakuniy ma'lumotlarni saqlaymiz
    db = SessionLocal()
    try:
        complete_workout_session(
            db=db,
            session_id=session_id,
            total_duration=total_duration,
            completed_count=completed_count
        )
    finally:
        db.close()

    # Statistika
    completion_rate = (completed_count / total_exercises) * 100 if total_exercises > 0 else 0
    minutes = total_duration // 60
    seconds = total_duration % 60

    message_text = (
        f"🎉 <b>Workout yakunlandi!</b>\n\n"
        f"✅ Bajarildi: <b>{completed_count}/{total_exercises}</b> mashq\n"
        f"⏱ Umumiy vaqt: <b>{minutes}:{seconds:02d}</b>\n"
        f"📊 Bajarilish: <b>{completion_rate:.0f}%</b>\n\n"
    )

    # Motivatsion xabar
    if completion_rate == 100:
        message_text += "🏆 <b>Mukammal!</b> Barcha mashqlarni bajardingiz!\n"
    elif completion_rate >= 80:
        message_text += "💪 <b>Ajoyib!</b> Zo'r natija!\n"
    elif completion_rate >= 50:
        message_text += "👍 <b>Yaxshi!</b> Davom eting!\n"
    else:
        message_text += "💪 <b>Boshlang'ich!</b> Keyingi safar yaxshiroq bo'ladi!\n"

    message_text += "\n📊 Progressingizni ko'rish uchun: <b>My Progress</b>"

    await message.answer(message_text)
    await state.clear()