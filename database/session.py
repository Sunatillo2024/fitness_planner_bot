"""
DEPRECATED: Bu fayl endi ishlatilmaydi.
Barcha operatsiyalar database/crud.py da amalga oshiriladi.

Eski kod backward compatibility uchun saqlanadi.
"""

from sqlalchemy.orm import Session
from database.models import User


def create_user(db: Session, telegram_id: int, user_data: dict, selected_goal: str):
    """
    DEPRECATED: create_user_full() dan foydalaning (database/crud.py)

    Foydalanuvchini DB ga saqlaydi yoki update qiladi.
    """
    from database.crud import create_user_full

    return create_user_full(
        db=db,
        telegram_id=telegram_id,
        full_name=user_data.get("name"),
        age=user_data.get("age"),
        weight=user_data.get("weight"),
        height=user_data.get("height"),
        goal=selected_goal
    )