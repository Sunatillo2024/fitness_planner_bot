from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import html

from States.user_state import UserInfo
from keyboards.replay_kbt import fitness_reply_menu, goals_keyboard
from database.db import SessionLocal
from database.crud import get_user_by_telegram_id, create_user_full

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    """Start buyrug'i - foydalanuvchini tekshirish va ro'yxatdan o'tkazish"""
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name

    # Database'dan foydalanuvchini tekshirish
    db = SessionLocal()
    try:
        user = get_user_by_telegram_id(db, telegram_id)
    finally:
        db.close()

    if user and user.age and user.weight and user.height and user.goal:
        # Foydalanuvchi to'liq ro'yxatdan o'tgan
        await message.answer(
            f"👋 Xush kelibsiz, {html.bold(full_name)}!\n\n"
            f"✅ Sizning profilingiz allaqachon mavjud.\n\n"
            f"📊 <b>Profil ma'lumotlari:</b>\n"
            f"   • Ism: {user.full_name}\n"
            f"   • Yosh: {user.age}\n"
            f"   • Vazn: {user.weight} kg\n"
            f"   • Bo'y: {user.height} cm\n\n"
            f"💪 Quyidagi menyudan kerakli bo'limni tanlang!",
            reply_markup=fitness_reply_menu()
        )
        return

    # Yangi foydalanuvchi yoki to'liq ma'lumot yo'q
    gif_url = "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif"
    caption = (
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "🏋️‍♂️ <b>Fitness Planner Bot</b>ga xush kelibsiz!\n\n"
        "✨ Bu yerda siz:\n"
        "   • 💪 Mashq rejalarini olasiz\n"
        "   • 📊 Progressingizni kuzatasiz\n"
        "   • 🥗 Ovqatlanish maslahatlari olasiz\n"
        "   • 🍎 Meal planlar topasiz\n\n"
        "🎯 Boshlash uchun profilingizni to'ldiring!"
    )

    await message.answer(
        f"👋 Salom, {html.bold(full_name)}!",
        reply_markup=fitness_reply_menu()
    )

    await message.answer_animation(animation=gif_url, caption=caption)

    await message.answer(
        "📝 <b>1/5 - Ismingiz</b>\n\n"
        "Iltimos, ismingizni kiriting:"
    )

    await state.set_state(UserInfo.name)


@router.message(StateFilter(UserInfo.name))
async def process_name(message: Message, state: FSMContext):
    """Ism qabul qilish"""
    name = message.text.strip()

    if len(name) < 2:
        await message.answer(
            "❌ Ism juda qisqa!\n"
            "Kamida 2 ta harf bo'lishi kerak."
        )
        return

    if len(name) > 50:
        await message.answer(
            "❌ Ism juda uzun!\n"
            "50 ta belgidan kam bo'lishi kerak."
        )
        return

    await state.update_data(name=name)
    await message.answer(
        f"✅ Yaxshi, <b>{name}</b>!\n\n"
        f"📝 <b>2/5 - Yoshingiz</b>\n\n"
        f"Yoshingizni kiriting (raqamda):"
    )
    await state.set_state(UserInfo.age)


@router.message(StateFilter(UserInfo.age))
async def process_age(message: Message, state: FSMContext):
    """Yosh qabul qilish"""
    try:
        age = int(message.text)
        if age < 10 or age > 100:
            await message.answer(
                "❌ Noto'g'ri yosh!\n"
                "10 dan 100 gacha bo'lgan son kiriting."
            )
            return
    except ValueError:
        await message.answer(
            "❌ Iltimos, faqat raqam kiriting!\n"
            "Masalan: <code>25</code>"
        )
        return

    await state.update_data(age=age)
    await message.answer(
        f"✅ Yosh: <b>{age}</b>\n\n"
        f"📝 <b>3/5 - Vazningiz</b>\n\n"
        f"⚖️ Vazningizni kiriting (kg):"
    )
    await state.set_state(UserInfo.weight)


@router.message(StateFilter(UserInfo.weight))
async def process_weight(message: Message, state: FSMContext):
    """Vazn qabul qilish"""
    try:
        weight = float(message.text.replace(",", "."))
        if weight < 30 or weight > 300:
            await message.answer(
                "❌ Noto'g'ri vazn!\n"
                "30 kg dan 300 kg gacha kiriting."
            )
            return
    except ValueError:
        await message.answer(
            "❌ Iltimos, raqam kiriting!\n"
            "Masalan: <code>70</code> yoki <code>70.5</code>"
        )
        return

    await state.update_data(weight=weight)
    await message.answer(
        f"✅ Vazn: <b>{weight} kg</b>\n\n"
        f"📝 <b>4/5 - Bo'yingiz</b>\n\n"
        f"📏 Bo'yingizni kiriting (cm):"
    )
    await state.set_state(UserInfo.height)


@router.message(StateFilter(UserInfo.height))
async def process_height(message: Message, state: FSMContext):
    """Bo'y qabul qilish"""
    try:
        height = float(message.text.replace(",", "."))
        if height < 100 or height > 250:
            await message.answer(
                "❌ Noto'g'ri bo'y!\n"
                "100 cm dan 250 cm gacha kiriting."
            )
            return
    except ValueError:
        await message.answer(
            "❌ Iltimos, raqam kiriting!\n"
            "Masalan: <code>175</code>"
        )
        return

    await state.update_data(height=height)

    # BMI hisoblash
    data = await state.get_data()
    weight = data.get("weight")
    bmi = weight / ((height / 100) ** 2)

    bmi_status = ""
    bmi_emoji = ""
    if bmi < 18.5:
        bmi_status = "Yengil vazn"
        bmi_emoji = "⚠️"
    elif bmi < 25:
        bmi_status = "Normal vazn"
        bmi_emoji = "✅"
    elif bmi < 30:
        bmi_status = "Ortiqcha vazn"
        bmi_emoji = "⚠️"
    else:
        bmi_status = "Semizlik"
        bmi_emoji = "❗"

    await message.answer(
        f"✅ Bo'y: <b>{height} cm</b>\n\n"
        f"📊 <b>Sizning BMI:</b> {bmi:.1f}\n"
        f"{bmi_emoji} <i>{bmi_status}</i>\n\n"
        f"📝 <b>5/5 - Maqsadingiz</b>\n\n"
        f"🎯 Maqsadingizni tanlang:",
        reply_markup=goals_keyboard
    )
    await state.set_state(UserInfo.goal)


@router.message(StateFilter(UserInfo.goal))
async def process_goal(message: Message, state: FSMContext):
    """Maqsad qabul qilish va saqlash"""
    goal_map = {
        "Weight Loss": "weight_loss",
        "Muscle Gain": "muscle_gain",
        "Healthy Life": "healthy_life"
    }

    selected_goal_key = goal_map.get(message.text)

    if not selected_goal_key:
        await message.answer(
            "❌ Iltimos, tugmalardan birini tanlang!",
            reply_markup=goals_keyboard
        )
        return

    user_data = await state.get_data()
    telegram_id = message.from_user.id

    # Database'ga saqlash
    db = SessionLocal()
    try:
        create_user_full(
            db=db,
            telegram_id=telegram_id,
            full_name=user_data.get("name"),
            age=user_data.get("age"),
            weight=user_data.get("weight"),
            height=user_data.get("height"),
            goal=selected_goal_key
        )
    finally:
        db.close()

    # Maqsadga mos xabar
    goal_messages = {
        "weight_loss": "📉 Vazn tashlash",
        "muscle_gain": "💪 Mushak oshirish",
        "healthy_life": "🌟 Sog'lom hayot"
    }

    goal_tips = {
        "weight_loss": "💡 <i>Kalloriya defitsiti va kardio muhim!</i>",
        "muscle_gain": "💡 <i>Yuqori protein va kuch mashqlari!</i>",
        "healthy_life": "💡 <i>Muvozanatli ovqatlanish va muntazam mashq!</i>"
    }

    await message.answer(
        f"🎉 <b>Profil muvaffaqiyatli saqlandi!</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 <b>Ism:</b> {user_data.get('name')}\n"
        f"📅 <b>Yosh:</b> {user_data.get('age')}\n"
        f"⚖️ <b>Vazn:</b> {user_data.get('weight')} kg\n"
        f"📏 <b>Bo'y:</b> {user_data.get('height')} cm\n"
        f"🎯 <b>Maqsad:</b> {goal_messages.get(selected_goal_key, 'Sog\'lom hayot')}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"{goal_tips.get(selected_goal_key, '')}\n\n"
        f"✅ Endi barcha funksiyalardan foydalanishingiz mumkin!",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "🏠 <b>Asosiy Menyu</b>\n\n"
        "Quyidagi bo'limlardan birini tanlang:\n\n"
        "💪 <b>Workout Plans</b> - Mashq rejalari\n"
        "🏋️ <b>Exercises</b> - Mashqlar katalogi\n"
        "📊 <b>My Progress</b> - Statistikangiz\n"
        "🥗 <b>Nutrition Tips</b> - Ovqatlanish maslahatlari\n"
        "🍎 <b>Meal Plan</b> - Ovqatlanish rejasi\n"
        "❓ <b>Help</b> - Yordam",
        reply_markup=fitness_reply_menu()
    )

    await state.clear()