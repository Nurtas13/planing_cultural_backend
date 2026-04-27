from sqlalchemy import Column, Integer, String, Text, Date, Time, Float, DateTime
from sqlalchemy.sql import func
from app.data_access.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=True)
    image_url = Column(Text, nullable=True)
    price = Column(Float, default=0)
    max_participants = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())