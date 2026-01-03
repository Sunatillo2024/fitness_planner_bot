# 🏋️ Fitness Planner Bot

Telegram orqali shaxsiy fitness planner - mashqlar, ovqatlanish va progress tracking!

## 🎯 Asosiy Imkoniyatlar

### 💪 Workout Plans
- **Home Workout** - uyda bajarish mumkin bo'lgan mashqlar
- **Gym Workout** - sport zali uchun mashqlar
- Har bir mashq uchun **GIF animatsiya**
- **60-90 soniyalik timer** har mashq uchun
- Progress avtomatik **database ga saqlanadi**

### 🏋️ Exercises
- Mashqlar katalogi
- GIF ko'rinishda demonstratsiya
- Har mashq uchun batafsil tavsif

### 📊 My Progress
- Oxirgi **7 kunlik statistika**
- Umumiy workoutlar soni
- Sarflangan vaqt hisobi
- Kunlar bo'yicha ajratilgan ko'rinish

### 🥗 Nutrition Tips
- Tasodifiy foydali maslahatlar
- Ovqatlanish bo'yicha yo'riqnomalar
- Har safar yangi maslahat

### 🍎 Meal Plan
- **Muvozanatli reja** - oddiy rejim
- **Vazn tashlash rejasi** - diet
- **Mushak oshirish rejasi** - bulking

### ❓ Help
- Bot bo'yicha to'liq yo'riqnoma
- Har bir funksiya tavsifi

## 🚀 O'rnatish

### 1. Repository ni clone qiling
```bash
git clone https://github.com/username/fitness_planner_bot.git
cd fitness_planner_bot
```

### 2. Virtual environment yarating
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Kerakli paketlarni o'rnating
```bash
pip install -r requirements.txt
```

### 4. .env faylini sozlang
```bash
cp .env.example .env
```

`.env` faylini oching va bot tokenini kiriting:
```
BOT_TOKEN=your_telegram_bot_token_here
```

### 5. Botni ishga tushiring
```bash
python bot.py
```

## 📁 Loyiha Strukturasi

```
fitness_planner_bot/
├── bot.py                    # Asosiy fayl
├── config.py                 # Konfiguratsiya
├── requirements.txt          # Dependencies
├── .env                      # Environment variables (gitignore)
├── .env.example             # Namuna env fayl
├── States/
│   ├── __init__.py
│   └── user_state.py        # FSM states
├── database/
│   ├── __init__.py
│   ├── db.py                # Database connection
│   ├── models.py            # SQLAlchemy models
│   └── session.py           # DB helper functions
├── handlers/
│   ├── __init__.py
│   ├── start_hl.py          # /start va user registration
│   ├── workout_hl.py        # Workout Plans handler
│   ├── exercises_hl.py      # Exercises handler
│   ├── progress_hl.py       # My Progress handler
│   ├── nutrition_hl.py      # Nutrition + Meal Plan
│   └── help_hl.py           # Help handler
└── keyboards/
    ├── __init__.py
    ├── inline_kbt.py        # Inline keyboards
    └── replay_kbt.py        # Reply keyboards
```

## 🗄️ Database Struktura

### Users
- `telegram_id` - Foydalanuvchi ID
- `name`, `age`, `weight`, `height` - Shaxsiy ma'lumotlar
- `goal` - Maqsad (weight_loss, muscle_gain, healthy_life)

### WorkoutSession
- `telegram_id` - Foydalanuvchi
- `total_duration` - Umumiy vaqt (soniyalarda)
- `completed_at` - Tugallangan sana

### WorkoutLog
- `session_id` - Session ID
- `exercise_name` - Mashq nomi
- `reps` - Takrorlash (3x10)
- `duration_seconds` - Davomiyligi

## 🎮 Qanday Ishlaydi?

1. **Foydalanuvchi** `/start` buyrug'ini yuboradi
2. **Bot** ma'lumotlarni yig'adi (ism, yosh, vazn, bo'y, maqsad)
3. **Asosiy menyu** ko'rsatiladi
4. **Workout Plans** ni tanlasa:
   - Home yoki Gym workoutni tanlaydi
   - Har bir mashq uchun GIF + timer
   - Next Exercise / Rest / Finish tugmalari
5. **Finish** bosilganda barcha ma'lumotlar DB ga saqlanadi
6. **My Progress** orqali statistikani ko'rish mumkin

## 🔧 Texnologiyalar

- **Python 3.10+**
- **aiogram 3.x** - Telegram Bot framework
- **SQLAlchemy** - ORM
- **SQLite** - Database (Production uchun PostgreSQL tavsiya etiladi)

## 📝 ToDo / Kelajakdagi Rejalar

- [ ] 7 kunlik challenge
- [ ] Streak (ketma-ket kunlar)
- [ ] Grafik progress
- [ ] Calories calculator
- [ ] Premium workout plans
- [ ] Social features (friends, leaderboard)

## 📧 Muallif

**Fitness Planner Bot**  
Savollar yoki takliflar uchun:  
Telegram: [@yourusername]

## 📄 Litsenziya

MIT License - ishlatishingiz mumkin!

---

⭐ Agar loyiha yoqsa, GitHub'da star qo'ying!
