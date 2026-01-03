from sqlalchemy.orm import Session
from database.models import User, WorkoutSession, ExerciseLog, WeightProgress
from datetime import datetime, timedelta
from typing import Optional, List


# ============ USER OPERATIONS ============
def get_or_create_user(db: Session, telegram_id: int, full_name: str = None) -> User:
    """
    Foydalanuvchini olish yoki yaratish
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user_by_telegram_id(db: Session, telegram_id: int) -> Optional[User]:
    """
    Telegram ID bo'yicha foydalanuvchini olish
    """
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def update_user_profile(db: Session, telegram_id: int, **kwargs) -> User:
    """
    Foydalanuvchi profilini yangilash
    """
    user = get_or_create_user(db, telegram_id)

    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def create_user_full(db: Session, telegram_id: int, full_name: str, age: int,
                     weight: float, height: float, goal: str) -> User:
    """
    To'liq foydalanuvchi ma'lumotlarini yaratish/yangilash
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            age=age,
            weight=weight,
            height=height,
            goal=goal
        )
        db.add(user)
    else:
        user.full_name = full_name
        user.age = age
        user.weight = weight
        user.height = height
        user.goal = goal
        user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user


# ============ WORKOUT SESSION OPERATIONS ============
def create_workout_session(db: Session, telegram_id: int, workout_type: str,
                           total_exercises: int) -> WorkoutSession:
    """
    Yangi workout session yaratish
    """
    user = get_or_create_user(db, telegram_id)

    session = WorkoutSession(
        user_id=user.id,
        workout_type=workout_type,
        total_exercises=total_exercises,
        completed_exercises=0,
        total_duration=0,
        started_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def complete_workout_session(db: Session, session_id: int, total_duration: int,
                             completed_count: int) -> WorkoutSession:
    """
    Workout sessionni yakunlash
    """
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if session:
        session.completed_exercises = completed_count
        session.total_duration = total_duration
        session.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
    return session


def get_user_workout_sessions(db: Session, telegram_id: int, days: int = 7) -> List[WorkoutSession]:
    """
    Foydalanuvchining oxirgi N kunlik workout sessionlarini olish
    """
    user = get_user_by_telegram_id(db, telegram_id)
    if not user:
        return []

    date_from = datetime.utcnow() - timedelta(days=days)

    return db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user.id,
        WorkoutSession.completed_at.isnot(None),
        WorkoutSession.completed_at >= date_from
    ).order_by(WorkoutSession.completed_at.desc()).all()


def get_user_total_stats(db: Session, telegram_id: int) -> dict:
    """
    Foydalanuvchining umumiy statistikasi
    """
    user = get_user_by_telegram_id(db, telegram_id)
    if not user:
        return {
            "total_workouts": 0,
            "total_time": 0,
            "total_exercises": 0
        }

    sessions = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user.id,
        WorkoutSession.completed_at.isnot(None)
    ).all()

    return {
        "total_workouts": len(sessions),
        "total_time": sum(s.total_duration for s in sessions),
        "total_exercises": sum(s.completed_exercises for s in sessions)
    }


# ============ EXERCISE LOG OPERATIONS ============
def add_exercise_log(db: Session, session_id: int, exercise_name: str,
                     sets_reps: str, duration: int) -> ExerciseLog:
    """
    Mashq logini qo'shish
    """
    log = ExerciseLog(
        session_id=session_id,
        exercise_name=exercise_name,
        sets_reps=sets_reps,
        duration=duration,
        completed=1
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_session_exercises(db: Session, session_id: int) -> List[ExerciseLog]:
    """
    Session uchun barcha mashqlarni olish
    """
    return db.query(ExerciseLog).filter(
        ExerciseLog.session_id == session_id
    ).order_by(ExerciseLog.logged_at).all()


# ============ WEIGHT PROGRESS OPERATIONS ============
def add_weight_record(db: Session, telegram_id: int, weight: float,
                      note: str = None) -> WeightProgress:
    """
    Vazn o'lchovini qo'shish
    """
    user = get_or_create_user(db, telegram_id)

    record = WeightProgress(
        user_id=user.id,
        weight=weight,
        note=note
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_weight_history(db: Session, telegram_id: int, days: int = 30) -> List[WeightProgress]:
    """
    Vazn tarixini olish
    """
    user = get_user_by_telegram_id(db, telegram_id)
    if not user:
        return []

    date_from = datetime.utcnow() - timedelta(days=days)

    return db.query(WeightProgress).filter(
        WeightProgress.user_id == user.id,
        WeightProgress.recorded_at >= date_from
    ).order_by(WeightProgress.recorded_at.desc()).all()


def get_latest_weight(db: Session, telegram_id: int) -> Optional[WeightProgress]:
    """
    Eng oxirgi vazn o'lchovini olish
    """
    user = get_user_by_telegram_id(db, telegram_id)
    if not user:
        return None

    return db.query(WeightProgress).filter(
        WeightProgress.user_id == user.id
    ).order_by(WeightProgress.recorded_at.desc()).first()