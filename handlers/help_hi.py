from aiogram import Router, F
from aiogram.types import Message

help_router = Router()


@help_router.message(F.text == "❓ Help")
async def help_handler(message: Message):
    """Bot haqida to'liq ma'lumot"""
    help_text = """
🤖 <b>Fitness Planner Bot - To'liq Yo'riqnoma</b>

━━━━━━━━━━━━━━━━━━━━━━

<b>💪 WORKOUT PLANS</b>
To'liq mashq rejalari bilan ishlash

<b>🏠 Home Workout:</b>
   • Uy uchun 5 ta mashq
   • Hech qanday asbob kerak emas
   • ~20-25 daqiqa

<b>🏋️ Gym Workout:</b>
   • Zal uchun 5 ta mashq
   • Professional uskunalar bilan
   • ~30-35 daqiqa

<b>Qanday ishlaydi?</b>
1️⃣ Workout turini tanlang
2️⃣ Har mashq uchun GIF ko'rsatiladi
3️⃣ Timer boshlang (60-90 soniya)
4️⃣ Keyingi mashqqa o'ting
5️⃣ Tugagach barcha ma'lumot saqlanadi

━━━━━━━━━━━━━━━━━━━━━━

<b>🏋️ EXERCISES</b>
Alohida mashqlar katalogi

• Home va Gym mashqlar ro'yxati
• Har biri GIF animatsiya bilan
• Batafsil tavsiflar
• Qaysi mushak ishlashi haqida ma'lumot

━━━━━━━━━━━━━━━━━━━━━━

<b>📊 MY PROGRESS</b>
Sizning natijalaringizni kuzatish

<b>🏋️ Workout Statistika:</b>
   • Oxirgi 7 kunlik workoutlar
   • Umumiy statistika
   • Haftalik xulosasa
   • Motivatsion xabarlar

<b>⚖️ Vazn Tarixingiz:</b>
   • Vazn o'zgarishini kuzatish
   • BMI hisoblash
   • Oxirgi 30 kunlik grafik
   • Yangi vazn qo'shish

━━━━━━━━━━━━━━━━━━━━━━

<b>🥗 NUTRITION TIPS</b>
Foydali ovqatlanish maslahatlari

• 15+ turli maslahat
• Kundalik yangi tip
• Oddiy va tushunarli
• Amaliy tavsiyalar

<b>Mavzular:</b>
💧 Suv ichish
🥗 Sabzavotlar
🍗 Protein
🥑 Foydali yog'lar
😴 Uyqu va hokazo...

━━━━━━━━━━━━━━━━━━━━━━

<b>🍎 MEAL PLAN</b>
Kunlik ovqatlanish rejalari

<b>3 xil reja:</b>

<b>🍽 Muvozanatli:</b>
   • Oddiy sog'lom reja
   • Barcha uchun mos
   • To'liq ovqatlar

<b>📉 Vazn Tashlash:</b>
   • Kalloriya defitsiti
   • Yengil ovqatlar
   • Sabzavot ko'proq

<b>💪 Mushak Oshirish:</b>
   • Yuqori protein
   • Ko'p ovqat
   • 6-7 marta ovqatlanish

Har bir reja uchun:
• Nonushta, tushlik, kechki ovqat
• Snacklar
• Porsiyalar va ingredientlar
• Tavsiyalar

━━━━━━━━━━━━━━━━━━━━━━

<b>🎯 BOSHLASH UCHUN:</b>

1️⃣ Profilingizni to'ldiring
   /start buyrug'i orqali

2️⃣ Mashq boshlang
   💪 Workout Plans → Home/Gym

3️⃣ Timer bilan bajaring
   Har mashq uchun 60-90 soniya

4️⃣ Natijani ko'ring
   📊 My Progress orqali

━━━━━━━━━━━━━━━━━━━━━━

<b>💡 MASLAHATLAR:</b>

✅ Har kuni 20-30 daqiqa mashq qiling
✅ Suv iching (2-3 litr)
✅ To'g'ri ovqatlaning
✅ Progressni kuzatib boring
✅ Muntazam bo'ling - muvaffaqiyat!

━━━━━━━━━━━━━━━━━━━━━━

<b>❓ SAVOL-JAVOB:</b>

<b>Q:</b> Workout ma'lumotlari saqlanadimi?
<b>A:</b> Ha, har bir session DB ga saqlanadi

<b>Q:</b> Progressni qanday ko'raman?
<b>A:</b> 📊 My Progress bo'limidan

<b>Q:</b> Timer to'xtatish mumkinmi?
<b>A:</b> Ha, "Dam Olish" tugmasini bosing

<b>Q:</b> Vazn qo'shish kerakmi?
<b>A:</b> Ixtiyoriy, lekin kuzatish foydali

━━━━━━━━━━━━━━━━━━━━━━

<b>🆘 YORDAM KERAKMI?</b>

Agar savol yoki muammo bo'lsa:
• Botni qayta boshlang: /start
• Barcha buyruqlar ishlaydi

━━━━━━━━━━━━━━━━━━━━━━

<b>🎉 OMAD TILAYMIZ!</b>

Fitness yo'lingizda muvaffaqiyatlar!
Har bir qadam muhim! 💪

<i>Fitness Planner Bot © 2024</i>
    """

    await message.answer(help_text)