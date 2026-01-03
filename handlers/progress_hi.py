from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.db import SessionLocal
from database.crud import (
    get_user_workout_sessions,
    get_user_total_stats,
    get_user_by_telegram_id,
    add_weight_record,
    get_weight_history
)
from keyboards.inline_kbt import get_progress_menu_keyboard, get_weight_tracking_keyboard
from datetime import datetime

progress_router = Router()


class WeightState(StatesGroup):
    entering_weight = State()


@progress_router.message(F.text == "📊 My Progress")
async def show_progress_menu(message: Message):
    """Progress menyu"""
    await message.answer(
        "📊 <b>Progress bo'limi</b>\n\n"
        "Qaysi ma'lumotni ko'rmoqchisiz?",
        reply_markup=get_progress_menu_keyboard()
    )


@progress_router.callback_query(F.data == "progress_workout")
async def show_workout_stats(callback: CallbackQuery):
    """Workout statistikasi"""
    telegram_id = callback.from_user.id

    db = SessionLocal()
    try:
        # Oxirgi 7 kunlik ma'lumotlar
        sessions = get_user_workout_sessions(db, telegram_id, days=7)

        # Umumiy statistika
        total_stats = get_user_total_stats(db, telegram_id)

        if not sessions and total_stats['total_workouts'] == 0:
            await callback.message.edit_text(
                "📊 <b>Workout Statistika</b>\n\n"
                "❌ Hali hech qanday workout bajarmagansiz.\n\n"
                "💪 <b>Workout Plans</b> orqali boshlang!",
                reply_markup=get_progress_menu_keyboard()
            )
            return

        # Umumiy statistika
        total_time_min = total_stats['total_time'] // 60
        avg_time = total_time_min // total_stats['total_workouts'] if total_stats['total_workouts'] > 0 else 0

        response = (
            f"📊 <b>Workout Statistika</b>\n\n"
            f"🏆 <b>Barcha vaqt:</b>\n"
            f"   • Workoutlar: <b>{total_stats['total_workouts']}</b> ta\n"
            f"   • Mashqlar: <b>{total_stats['total_exercises']}</b> ta\n"
            f"   • Umumiy vaqt: <b>{total_time_min}</b> daqiqa\n"
            f"   • O'rtacha: <b>{avg_time}</b> daq/workout\n\n"
        )

        if sessions:
            response += f"📅 <b>Oxirgi 7 kun:</b>\n\n"

            for session in sessions[:7]:
                date_str = session.completed_at.strftime("%d.%m.%Y")
                time_str = session.completed_at.strftime("%H:%M")
                duration_min = session.total_duration // 60
                workout_emoji = "🏠" if session.workout_type == "home" else "🏋️"

                completion = (
                            session.completed_exercises / session.total_exercises * 100) if session.total_exercises > 0 else 0

                response += (
                    f"{workout_emoji} <b>{date_str}</b> • {time_str}\n"
                    f"   ✅ {session.completed_exercises}/{session.total_exercises} mashq"
                    f" • ⏱ {duration_min} daq • 📊 {completion:.0f}%\n\n"
                )

            # Haftalik summary
            week_workouts = len(sessions)
            week_total_time = sum(s.total_duration for s in sessions) // 60
            week_exercises = sum(s.completed_exercises for s in sessions)

            response += (
                f"📈 <b>Haftalik xulosasa:</b>\n"
                f"   • <b>{week_workouts}</b> workout\n"
                f"   • <b>{week_exercises}</b> mashq\n"
                f"   • <b>{week_total_time}</b> daqiqa\n\n"
            )

            # Motivatsiya
            if week_workouts >= 5:
                response += "🏆 <b>Zo'r!</b> Siz haftada 5+ workout qildingiz!"
            elif week_workouts >= 3:
                response += "💪 <b>Ajoyib!</b> Maqsadga yaqinlashdingiz!"
            else:
                response += "📌 <b>Eslatma:</b> Haftada 3-4 workout tavsiya etiladi!"

        await callback.message.edit_text(
            response,
            reply_markup=get_progress_menu_keyboard()
        )

    finally:
        db.close()


@progress_router.callback_query(F.data == "progress_weight")
async def show_weight_stats(callback: CallbackQuery):
    """Vazn statistikasi"""
    telegram_id = callback.from_user.id

    db = SessionLocal()
    try:
        user = get_user_by_telegram_id(db, telegram_id)
        weight_history = get_weight_history(db, telegram_id, days=30)

        if not user:
            await callback.message.edit_text(
                "❌ Foydalanuvchi ma'lumotlari topilmadi.\n"
                "/start buyrug'ini qayta yuboring.",
                reply_markup=get_progress_menu_keyboard()
            )
            return

        response = f"⚖️ <b>Vazn Tarixingiz</b>\n\n"

        # Joriy vazn
        if user.weight:
            response += f"📊 <b>Boshlang'ich vazn:</b> {user.weight} kg\n"

            if user.height:
                bmi = user.weight / ((user.height / 100) ** 2)
                response += f"📏 <b>BMI:</b> {bmi:.1f}"

                if bmi < 18.5:
                    response += " (Yengil)\n"
                elif bmi < 25:
                    response += " (Normal)\n"
                elif bmi < 30:
                    response += " (Ortiqcha)\n"
                else:
                    response += " (Semizlik)\n"

        # Vazn tarixi
        if weight_history:
            response += f"\n📅 <b>Oxirgi 30 kun:</b>\n\n"

            for record in weight_history[:10]:
                date_str = record.recorded_at.strftime("%d.%m.%Y")
                response += f"• <b>{date_str}:</b> {record.weight} kg"
                if record.note:
                    response += f" - {record.note}"
                response += "\n"

            # O'zgarish
            if len(weight_history) >= 2:
                latest = weight_history[0].weight
                oldest = weight_history[-1].weight
                change = latest - oldest

                response += f"\n📈 <b>O'zgarish:</b> "
                if change > 0:
                    response += f"+{change:.1f} kg ⬆️"
                elif change < 0:
                    response += f"{change:.1f} kg ⬇️"
                else:
                    response += "O'zgarish yo'q"
        else:
            response += "\n\n💡 Vazningizni kuzatib boring!"

        response += "\n\n➕ Yangi vazn qo'shish uchun tugmani bosing."

        await callback.message.edit_text(
            response,
            reply_markup=get_weight_tracking_keyboard()
        )

    finally:
        db.close()


@progress_router.callback_query(F.data == "add_weight")
async def add_weight_prompt(callback: CallbackQuery, state: FSMContext):
    """Vazn qo'shish so'rovi"""
    await callback.message.edit_text(
        "⚖️ <b>Yangi vazn kiritish</b>\n\n"
        "Vazningizni kiriting (kg):\n"
        "Masalan: <code>75.5</code>"
    )
    await state.set_state(WeightState.entering_weight)


@progress_router.message(WeightState.entering_weight)
async def save_weight(message: Message, state: FSMContext):
    """Vaznni saqlash"""
    try:
        weight = float(message.text.replace(",", "."))

        if weight < 30 or weight > 300:
            await message.answer(
                "❌ Noto'g'ri qiymat!\n"
                "30 kg dan 300 kg gacha bo'lgan son kiriting."
            )
            return

        db = SessionLocal()
        try:
            add_weight_record(
                db=db,
                telegram_id=message.from_user.id,
                weight=weight
            )
        finally:
            db.close()

        await message.answer(
            f"✅ Vazn saqlandi: <b>{weight} kg</b>\n\n"
            f"📊 Progressingizni ko'rish uchun:\n"
            f"<b>My Progress → Weight Tracking</b>"
        )

        await state.clear()

    except ValueError:
        await message.answer(
            "❌ Noto'g'ri format!\n"
            "Faqat raqam kiriting. Masalan: <code>75.5</code>"
        )


@progress_router.callback_query(F.data == "progress_back")
async def back_to_progress_menu(callback: CallbackQuery):
    """Progress menyuga qaytish"""
    await show_progress_menu(callback.message)