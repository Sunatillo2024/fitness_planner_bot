from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    goal = Column(String, nullable=True)  # weight_loss, muscle_gain, healthy_life
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workout_sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")
    weight_progress = relationship("WeightProgress", back_populates="user", cascade="all, delete-orphan")


class WorkoutSession(Base):
    """
    Har bir to'liq workout session uchun
    """
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    workout_type = Column(String)  # home, gym
    total_exercises = Column(Integer)  # jami mashqlar soni
    completed_exercises = Column(Integer)  # bajarilgan mashqlar
    total_duration = Column(Integer)  # soniyalarda
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="workout_sessions")
    exercise_logs = relationship("ExerciseLog", back_populates="session", cascade="all, delete-orphan")


class ExerciseLog(Base):
    """
    Har bir workout session ichidagi alohida mashqlar
    """
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id", ondelete="CASCADE"))
    exercise_name = Column(String, nullable=False)
    sets_reps = Column(String)  # masalan "3x10"
    duration = Column(Integer)  # timer davomiyligi
    completed = Column(Integer, default=1)  # bajarildi yoki yo'q
    logged_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    session = relationship("WorkoutSession", back_populates="exercise_logs")

class Exercise(Base):
    """
    Mashqlar ma'lumotlar bazasi
    """
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    emoji = Column(String, nullable=True)
    gif_url = Column(String, nullable=True)
    muscles = Column(String, nullable=True)
    sets_reps = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    tips = Column(JSON, nullable=True)  # List sifatida saqlanadi
    exercise_type = Column(String, nullable=False)  # 'home' or 'gym'
    created_at = Column(DateTime, default=datetime.utcnow)


class WeightProgress(Base):
    """
    Foydalanuvchining vazn o'zgarishi tarixi
    """
    __tablename__ = "weight_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    weight = Column(Float, nullable=False)
    note = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="weight_progress")