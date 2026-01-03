# ===== 1. database/models.py ga qo'shing =====

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.orm.session import Session

from database.models import Exercise
from typing import List

HOME_EXERCISES = [
    {
        "name": "Push-ups",
        "emoji": "💪",
        "gif": "https://media.giphy.com/media/ZeAXZfK2v3z6hmMZEj/giphy.gif",
        "muscles": "Chest, Triceps, Shoulders",
        "sets_reps": "3 sets × 10-15 reps",
        "description": "Ko'krak, qo'l va yelka mushaklarini kuchaytiradi. Klassik va samarali mashq.",
        "tips": [
            "Tanangiz to'g'ri chiziqda bo'lsin",
            "Tirsak 45° burchakda",
            "Nafas to'g'ri oling"
        ]
    },
    {
        "name": "Squats",
        "emoji": "🦵",
        "gif": "https://media.giphy.com/media/1qfDU4MJv9xoGtRKvh/giphy.gif",
        "muscles": "Quads, Glutes, Hamstrings",
        "sets_reps": "3 sets × 12-20 reps",
        "description": "Oyoqlar va dumba mushaklarini rivojlantiradi. Eng asosiy mashqlardan biri.",
        "tips": [
            "Tizza oyoq barmog'idan oshmasin",
            "Orqa to'g'ri",
            "90° gacha tushing"
        ]
    },
    {
        "name": "Sit-ups",
        "emoji": "🔥",
        "gif": "https://media.giphy.com/media/2A75RyXVzzSI2bx4Gj/giphy.gif",
        "muscles": "Abs, Core",
        "sets_reps": "3 sets × 15-20 reps",
        "description": "Qorin mushaklarini mustahkamlaydi va core kuchini oshiradi.",
        "tips": [
            "Qo'llarni boshda ushlamang",
            "Mushakni sezib bajaring",
            "Tez-tez nafas oling"
        ]
    },
    {
        "name": "Plank",
        "emoji": "⚡",
        "gif": "https://media.giphy.com/media/3o7TKPATxjbMM6l8Mo/giphy.gif",
        "muscles": "Full Core, Shoulders",
        "sets_reps": "3 sets × 30-60 sec",
        "description": "Core barqarorlik va kuchini oshiradi. Statik mashq.",
        "tips": [
            "Tanangiz to'g'ri chiziqda",
            "Dumba yuqoriga ko'tarilmasin",
            "Nafas to'xtamang"
        ]
    },
    {
        "name": "Jumping Jacks",
        "emoji": "❤️",
        "gif": "https://media.giphy.com/media/26u4b45b8KlgAB7iM/giphy.gif",
        "muscles": "Full Body Cardio",
        "sets_reps": "3 sets × 30-50 reps",
        "description": "Kardio va endurance oshirish uchun. Butun tanani ishlatadi.",
        "tips": [
            "Ritm ushlab turing",
            "Yuqoriga sakrang",
            "Qo'llarni to'liq oching"
        ]
    },
    {
        "name": "Lunges",
        "emoji": "🦵",
        "gif": "https://media.giphy.com/media/3oEjHUf7j0aFDce0dG/giphy.gif",
        "muscles": "Quads, Glutes",
        "sets_reps": "3 sets × 10 reps (har bir oyoq)",
        "description": "Oyoqlar va muvozanat uchun mukammal mashq.",
        "tips": [
            "Tizza 90° burchakda",
            "Orqa oyoq yerga tegmasin",
            "Muvozanatni saqlang"
        ]
    },
    {
        "name": "Mountain Climbers",
        "emoji": "🔥",
        "gif": "https://media.giphy.com/media/l0HlAgJTVaAPHEGdy/giphy.gif",
        "muscles": "Core, Cardio",
        "sets_reps": "3 sets × 20-30 reps",
        "description": "Kardio va core uchun dinamik mashq.",
        "tips": [
            "Tez harakat qiling",
            "Tanangiz to'g'ri",
            "Nafas ritmik"
        ]
    }
]

GYM_EXERCISES = [
    {
        "name": "Bench Press",
        "emoji": "💪",
        "gif": "https://media.giphy.com/media/3oEdva0KggGvBqB7Fe/giphy.gif",
        "muscles": "Chest, Triceps, Shoulders",
        "sets_reps": "4 sets × 8-12 reps",
        "description": "Ko'krak uchun eng asosiy va samarali mashq. Og'irlik bilan.",
        "tips": [
            "Spotter bilan ishlang",
            "Barni to'g'ri ushlangsiz",
            "To'liq amplitudada"
        ]
    },
    {
        "name": "Deadlift",
        "emoji": "🔥",
        "gif": "https://media.giphy.com/media/3oEjI5VtIhHvK37WYo/giphy.gif",
        "muscles": "Back, Legs, Core",
        "sets_reps": "4 sets × 5-8 reps",
        "description": "Butun tanani ishlatadigan kuchli mashq. Orqa va oyoqlar uchun.",
        "tips": [
            "Orqa har doim to'g'ri",
            "Yelkanlar orqada",
            "Texnikaga e'tibor bering"
        ]
    },
    {
        "name": "Lat Pulldown",
        "emoji": "💪",
        "gif": "https://media.giphy.com/media/26u4cqiYI30juCOGY/giphy.gif",
        "muscles": "Lats, Biceps",
        "sets_reps": "3 sets × 10-12 reps",
        "description": "Orqa mushaklar kengligi uchun. Pull-up ga alternativa.",
        "tips": [
            "Ko'krak sari tortinng",
            "Tirsak orqaga",
            "Mushakni sezib bajaring"
        ]
    },
    {
        "name": "Shoulder Press",
        "emoji": "⚡",
        "gif": "https://media.giphy.com/media/xT8qBbx0BXs6oc0lgs/giphy.gif",
        "muscles": "Shoulders, Triceps",
        "sets_reps": "3 sets × 8-12 reps",
        "description": "Yelka kuchi va hajmi uchun asosiy mashq.",
        "tips": [
            "O'tirgan holatda mos",
            "To'liq yuqoriga",
            "Boshni oldinga surmang"
        ]
    },
    {
        "name": "Barbell Rows",
        "emoji": "💪",
        "gif": "https://media.giphy.com/media/3oKIPlifLxdhyETJRK/giphy.gif",
        "muscles": "Back Thickness, Biceps",
        "sets_reps": "3 sets × 8-10 reps",
        "description": "Orqa qalinligi uchun. Kuchli mashq.",
        "tips": [
            "Orqa parallel",
            "Barni beliga tortinng",
            "Tirsak tanaga yaqin"
        ]
    },
    {
        "name": "Leg Press",
        "emoji": "🦵",
        "gif": "https://media.giphy.com/media/l0HlR3kHtkgFbYfD2/giphy.gif",
        "muscles": "Quads, Glutes",
        "sets_reps": "3 sets × 12-15 reps",
        "description": "Oyoqlar uchun xavfsiz va samarali mashq.",
        "tips": [
            "Oyoqlar yelka kengligida",
            "90° gacha tushing",
            "Tizza ichkariga ketmasin"
        ]
    },
    {
        "name": "Cable Flyes",
        "emoji": "💪",
        "gif": "https://media.giphy.com/media/3oEjHYAlLK4BZvkupq/giphy.gif",
        "muscles": "Chest",
        "sets_reps": "3 sets × 12-15 reps",
        "description": "Ko'krak mushaklar uchun izolyatsiya mashq.",
        "tips": [
            "Mushakni cho'zing",
            "Sekin va nazorat bilan",
            "Ko'krakni siqing"
        ]
    }
]

def create_exercise(db: Session, exercise_data: dict) -> Exercise:
    """
    Yangi mashq yaratish
    """
    exercise = Exercise(**exercise_data)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def get_exercises_by_type(db: Session, exercise_type: str) -> List[Exercise]:
    """
    Tur bo'yicha mashqlarni olish (home yoki gym)
    """
    return db.query(Exercise).filter(
        Exercise.exercise_type == exercise_type
    ).all()


def get_all_exercises(db: Session) -> List[Exercise]:
    """
    Barcha mashqlarni olish
    """
    return db.query(Exercise).all()


def get_exercise_by_name(db: Session, name: str) -> Exercise:
    """
    Nom bo'yicha mashq topish
    """
    return db.query(Exercise).filter(
        Exercise.name.ilike(f"%{name}%")
    ).first()


# ===== 3. Yangi fayl: populate_exercises.py =====
"""
Exercise ma'lumotlarini database'ga yuklash
Faqat bir marta ishga tushirish kerak
"""

from database.db import SessionLocal
from database.models import Exercise

HOME_EXERCISES = [
    # ... sizning HOME_EXERCISES ma'lumotlaringiz
]

GYM_EXERCISES = [
    # ... sizning GYM_EXERCISES ma'lumotlaringiz
]


def populate_exercises():
    """
    Barcha exercises'larni database'ga yuklash
    """
    db = SessionLocal()

    try:
        # Home exercises
        print("📥 Home exercises yuklanmoqda...")
        for ex in HOME_EXERCISES:
            existing = db.query(Exercise).filter(
                Exercise.name == ex['name']
            ).first()

            if not existing:
                exercise = Exercise(
                    name=ex['name'],
                    emoji=ex['emoji'],
                    gif_url=ex['gif'],
                    muscles=ex['muscles'],
                    sets_reps=ex['sets_reps'],
                    description=ex['description'],
                    tips=ex['tips'],  # JSON sifatida saqlanadi
                    exercise_type='home'
                )
                db.add(exercise)
                print(f"  ✅ {ex['name']} qo'shildi")
            else:
                print(f"  ⏭ {ex['name']} allaqachon mavjud")

        # Gym exercises
        print("\n📥 Gym exercises yuklanmoqda...")
        for ex in GYM_EXERCISES:
            existing = db.query(Exercise).filter(
                Exercise.name == ex['name']
            ).first()

            if not existing:
                exercise = Exercise(
                    name=ex['name'],
                    emoji=ex['emoji'],
                    gif_url=ex['gif'],
                    muscles=ex['muscles'],
                    sets_reps=ex['sets_reps'],
                    description=ex['description'],
                    tips=ex['tips'],
                    exercise_type='gym'
                )
                db.add(exercise)
                print(f"  ✅ {ex['name']} qo'shildi")
            else:
                print(f"  ⏭ {ex['name']} allaqachon mavjud")

        db.commit()
        print("\n✅ Barcha exercises muvaffaqiyatli yuklandi!")

    except Exception as e:
        print(f"\n❌ Xatolik: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("🏋️ Exercises Database Popolation")
    print("=" * 50)
    populate_exercises()
    print("=" * 50)