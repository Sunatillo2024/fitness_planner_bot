from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kbt import get_meal_plan_keyboard, get_nutrition_tips_keyboard
import random

nutrition_router = Router()

# Nutrition tips ma'lumotlar bazasi
NUTRITION_TIPS = [
    {
        "emoji": "💧",
        "title": "Suv Ichish",
        "tip": "Kuniga kamida 2-3 litr suv iching! Suv metabolizmni tezlashtiradi va organizm tozalanishiga yordam beradi."
    },
    {
        "emoji": "🥗",
        "title": "Sabzavotlar",
        "tip": "Har kuni kamida 5 xil rangdagi sabzavot iste'mol qiling. Har xil rang - har xil vitamin!"
    },
    {
        "emoji": "🍗",
        "title": "Protein",
        "tip": "Protein tanangiz uchun qurilish materiali! Har ovqatda protein manbai bo'lsin: tovuq, tuxum, baliq yoki dukkakli."
    },
    {
        "emoji": "🍎",
        "title": "Tez-tez Ovqatlaning",
        "tip": "Kuniga 4-5 marta kichik porsiyalarda ovqatlaning. Bu metabolizmni faol saqlaydi."
    },
    {
        "emoji": "🚫",
        "title": "Qand Kamaytiring",
        "tip": "Qand va gazlangan ichimliklarni kamaytiring. Ular bo'sh kaloriya va sog'liq uchun zararli."
    },
    {
        "emoji": "🥑",
        "title": "Foydali Yog'lar",
        "tip": "Avokado, yong'oq va zaytun moyi - bu foydali yog'lar. Ular yurak salomatligiga yordam qiladi."
    },
    {
        "emoji": "😴",
        "title": "Uyqu",
        "tip": "Yaxshi uyqu ham muhim! 7-8 soatlik sifatli uyqu mushak tiklanishi va vazn nazorati uchun zarur."
    },
    {
        "emoji": "🏃",
        "title": "Mashq va Ovqat",
        "tip": "Mashqdan 30-60 daqiqa oldin yengil ovqat yoki snack iste'mol qiling. Energiya uchun!"
    },
    {
        "emoji": "🍌",
        "title": "Pre-Workout Snack",
        "tip": "Mashqdan oldin banan - mukammal energiya manbai! Karbogidrat va kaliy bilan boy."
    },
    {
        "emoji": "🥚",
        "title": "Nonushta",
        "tip": "Nonushta - kunning eng muhim ovqati! Protein va murakkab karbogidrat bilan boshlang."
    },
    {
        "emoji": "🥤",
        "title": "Protein Shake",
        "tip": "Mashqdan keyin 30 daqiqa ichida protein shake yoki protein ovqati iste'mol qiling."
    },
    {
        "emoji": "🌾",
        "title": "To'liq Donli",
        "tip": "Oq non o'rniga to'liq donli mahsulotlarni tanlang. Ular ko'proq tola va vitaminlarga boy."
    },
    {
        "emoji": "🥜",
        "title": "Yong'oq",
        "tip": "Yong'oq - mukammal snack! Protein, foydali yog'lar va energiya bilan to'la."
    },
    {
        "emoji": "🐟",
        "title": "Baliq",
        "tip": "Haftada kamida 2 marta baliq iste'mol qiling. Omega-3 yog' kislotalari uchun!"
    },
    {
        "emoji": "🍵",
        "title": "Yashil Choy",
        "tip": "Yashil choy antioksidantlarga boy va metabolizmni tezlashtiradi. Kuniga 2-3 chashka."
    }
]

# Meal plans
MEAL_PLANS = {
    "balanced": {
        "emoji": "🍽",
        "name": "Muvozanatli Reja",
        "description": "Sog'lom va muvozanatli kunlik ovqatlanish",
        "breakfast": {
            "title": "🌅 Nonushta (07:00-09:00)",
            "items": [
                "🥚 3 ta tuxumdan omlet",
                "🍞 2 bo'lak to'liq donli non",
                "🥑 1/2 avokado",
                "🍊 1 ta apelsin",
                "☕ Kofe yoki choy (shakarsiz)"
            ]
        },
        "snack1": {
            "title": "🍎 Snack 1 (10:30-11:00)",
            "items": [
                "🍎 1 ta olma",
                "🥜 Bir hovuch yong'oq (bodom, yeryong'oq)"
            ]
        },
        "lunch": {
            "title": "☀️ Tushlik (13:00-14:00)",
            "items": [
                "🍗 200g gril tovuq ko'kragi",
                "🍚 150g qo'ng'ir guruch",
                "🥗 Katta aralash salat (pomidor, bodring, sabzi)",
                "🥒 Zaytun moyi bilan"
            ]
        },
        "snack2": {
            "title": "🥤 Snack 2 (16:00-17:00)",
            "items": [
                "🧀 100g past yog'li tvorog",
                "🍌 1 ta banan"
            ]
        },
        "dinner": {
            "title": "🌙 Kechki ovqat (19:00-20:00)",
            "items": [
                "🐟 150g bug'da pishirilgan baliq",
                "🥔 200g qovurilgan kartoshka",
                "🥦 Broccoli yoki boshqa sabzavot",
                "🥗 Yashil salat"
            ]
        }
    },
    "weight_loss": {
        "emoji": "📉",
        "name": "Vazn Tashlash Rejasi",
        "description": "Kalloriya defitsiti bilan sog'lom ovqatlanish",
        "breakfast": {
            "title": "🌅 Nonushta (07:00-09:00)",
            "items": [
                "🥣 60g oatmeal (suvda)",
                "🍓 100g berry (qulupnai, malina)",
                "🥄 1 choy qoshiq asal",
                "☕ Yashil choy"
            ]
        },
        "snack1": {
            "title": "🥕 Snack 1 (10:30-11:00)",
            "items": [
                "🥕 Sabzavot (sabzi, bodring)",
                "🥗 100g hummus"
            ]
        },
        "lunch": {
            "title": "☀️ Tushlik (13:00-14:00)",
            "items": [
                "🥗 Katta yashil salat",
                "🍗 150g gril tovuq",
                "🍅 Cherry pomidor, bodring",
                "🥒 Limon sharbati bilan"
            ]
        },
        "snack2": {
            "title": "🍏 Snack 2 (16:00-17:00)",
            "items": [
                "🍏 1 ta yashil olma",
                "🥤 Protein shake (agar kerak bo'lsa)"
            ]
        },
        "dinner": {
            "title": "🌙 Kechki ovqat (18:30-19:30)",
            "items": [
                "🐟 150g bug'da baliq (losos, tuna)",
                "🥒 Bodring va pomidor salati",
                "🥦 Bug'da sabzavotlar",
                "🍋 Limon bilan"
            ]
        }
    },
    "muscle_gain": {
        "emoji": "💪",
        "name": "Mushak Oshirish Rejasi",
        "description": "Yuqori protein va kalloriya bilan ovqatlanish",
        "breakfast": {
            "title": "🌅 Nonushta (07:00-09:00)",
            "items": [
                "🥚 5 ta tuxum (3 butun + 2 oqsi)",
                "🥓 100g tovuq sosis yoki bekfest",
                "🍞 3 bo'lak to'liq donli non",
                "🥑 1 ta avokado",
                "🥤 Protein shake"
            ]
        },
        "snack1": {
            "title": "🥜 Snack 1 (10:00-10:30)",
            "items": [
                "🥜 Ikki hovuch yong'oq aralashmasi",
                "🍌 2 ta banan",
                "🧈 Yong'oq moyi"
            ]
        },
        "lunch": {
            "title": "☀️ Tushlik (13:00-14:00)",
            "items": [
                "🥩 250g qo'y yoki mol go'shti",
                "🍝 200g pasta yoki guruch",
                "🧀 100g tvorog",
                "🥗 Aralash salat",
                "🥤 1 stakan sut"
            ]
        },
        "snack2": {
            "title": "💪 Pre-Workout (15:30-16:00)",
            "items": [
                "🍌 2 ta banan",
                "🥜 Yong'oq moyi",
                "☕ Kofe (agar kerak bo'lsa)"
            ]
        },
        "snack3": {
            "title": "🥤 Post-Workout (17:30-18:00)",
            "items": [
                "🥤 Protein shake (40-50g protein)",
                "🍌 1 ta banan",
                "🍯 1 osh qoshiq asal"
            ]
        },
        "dinner": {
            "title": "🌙 Kechki ovqat (19:30-20:30)",
            "items": [
                "🍗 300g tovuq ko'kragi",
                "🍚 200g qo'ng'ir guruch",
                "🥦 Sabzavotlar",
                "🥗 Salat zaytun moyi bilan",
                "🥛 1 stakan sut"
            ]
        },
        "snack4": {
            "title": "🌙 Uyqu Oldidan (22:00-22:30)",
            "items": [
                "🧀 150g tvorog",
                "🥜 Bir hovuch yong'oq"
            ]
        }
    }
}


@nutrition_router.message(F.text == "🥗 Nutrition Tips")
async def show_nutrition_tip(message: Message):
    """Tasodifiy nutrition tip ko'rsatish"""
    tip = random.choice(NUTRITION_TIPS)

    response = (
        f"{tip['emoji']} <b>{tip['title']}</b>\n\n"
        f"{tip['tip']}\n\n"
        f"💡 <i>Sog'lom ovqatlanish - sog'lom hayot!</i>"
    )

    await message.answer(
        response,
        reply_markup=get_nutrition_tips_keyboard()
    )


@nutrition_router.callback_query(F.data == "nutrition_tip")
async def show_another_tip(callback: CallbackQuery):
    """Yana bir tip ko'rsatish"""
    tip = random.choice(NUTRITION_TIPS)

    response = (
        f"{tip['emoji']} <b>{tip['title']}</b>\n\n"
        f"{tip['tip']}\n\n"
        f"💡 <i>Sog'lom ovqatlanish - sog'lom hayot!</i>"
    )

    await callback.message.edit_text(
        response,
        reply_markup=get_nutrition_tips_keyboard()
    )


@nutrition_router.message(F.text == "🍎 Meal Plan")
async def show_meal_plan_menu(message: Message):
    """Meal plan menyusini ko'rsatish"""
    await message.answer(
        "🍽 <b>Ovqatlanish Rejasini Tanlang</b>\n\n"
        "🍽 <b>Muvozanatli:</b> Oddiy sog'lom reja\n"
        "📉 <b>Vazn Tashlash:</b> Kalloriya defitsiti\n"
        "💪 <b>Mushak Oshirish:</b> Yuqori protein\n\n"
        "💡 Rejangizni tanlang:",
        reply_markup=get_meal_plan_keyboard()
    )


@nutrition_router.callback_query(F.data.startswith("meal_"))
async def show_meal_plan_detail(callback: CallbackQuery):
    """Tanlangan meal planni batafsil ko'rsatish"""
    plan_type = callback.data.replace("meal_", "")
    plan = MEAL_PLANS.get(plan_type)

    if not plan:
        await callback.answer("❌ Reja topilmadi", show_alert=True)
        return

    # Rejani formatlash
    response = (
        f"{plan['emoji']} <b>{plan['name']}</b>\n\n"
        f"<i>{plan['description']}</i>\n\n"
        f"{'=' * 30}\n\n"
    )

    for meal_key, meal_data in plan.items():
        if meal_key in ["emoji", "name", "description"]:
            continue

        response += f"<b>{meal_data['title']}</b>\n"
        for item in meal_data['items']:
            response += f"  • {item}\n"
        response += "\n"

    response += (
        f"{'=' * 30}\n\n"
        f"💡 <b>Maslahatlar:</b>\n"
        f"• Suv ichishni unutmang\n"
        f"• Ovqat orasida 3-4 soat tanaffus\n"
        f"• Porsiyalarni o'z vazningizga moslashtiring\n"
        f"• Mashqdan oldin va keyin to'g'ri ovqatlaning"
    )

    await callback.message.edit_text(
        response,
        reply_markup=get_meal_plan_keyboard()
    )


@nutrition_router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    await callback.message.delete()
    await callback.message.answer(
        "🏠 Asosiy menyu\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=None  # Reply keyboard avtomatik ko'rsatiladi
    )