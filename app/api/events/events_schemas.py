from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    location: str
    event_date: date
    event_time: Optional[time] = None
    image_url: Optional[str] = None
    price: float = 0
    max_participants: Optional[int] = None


class EventRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: str
    location: str
    event_date: date
    event_time: Optional[time] = None
    image_url: Optional[str] = None
    price: float
    max_participants: Optional[int] = None

    class Config:
        from_attributes = True