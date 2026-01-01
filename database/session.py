from sqlalchemy.orm import Session
from database.models import User


def create_user(db: Session, telegram_id: int, user_data: dict, selected_goal: str):
    """
    Foydalanuvchini DB ga saqlaydi yoki update qiladi.
    :param db: SQLAlchemy Session
    :param telegram_id: telegram user id
    :param user_data: dict {name, age, weight, height}
    :param selected_goal: str, masalan "weight_loss"
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(
            telegram_id=telegram_id,
            name=user_data.get("name"),
            age=user_data.get("age"),
            weight=user_data.get("weight"),
            height=user_data.get("height"),
            goal=selected_goal
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name = user_data.get("name")
        user.age = user_data.get("age")
        user.weight = user_data.get("weight")
        user.height = user_data.get("height")
        user.goal = selected_goal
        db.commit()

    return user
