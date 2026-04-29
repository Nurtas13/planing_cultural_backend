from pydantic import BaseModel
from typing import Optional

class RegistrationCreate(BaseModel):
    user_id: int
    event_id: int


class RegistrationUpdate(BaseModel):
    status: Optional[str] = None

class RegistrationRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str

    class Config:
        from_attributes = True

class UserRegistrationEventRead(BaseModel):
    registration_id: int
    event_id: int
    status: str
    title: str
    date: str
    location: str
    image_url: Optional[str] = None