from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# ВАЖНО: ИМПОРТ ВСЕХ МОДЕЛЕЙ НИЖЕ
from app.data_access.models.user import User
from app.data_access.models.event import Event
from app.data_access.models.registration import Registration