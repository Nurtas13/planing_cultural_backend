from pydantic import BaseModel


class RegistrationCreate(BaseModel):
    user_id: int
    event_id: int


class RegistrationRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str

    class Config:
        from_attributes = True