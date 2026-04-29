from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.models.registration import Registration

from app.data_access.models.event import Event

class RegistrationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_registration(self, registration_data):
        new_registration = Registration(**registration_data.model_dump())
        self.db.add(new_registration)
        await self.db.commit()
        await self.db.refresh(new_registration)
        return new_registration

    async def get_user_registrations(self, user_id: int):
        result = await self.db.execute(
            select(Registration).where(Registration.user_id == user_id)
        )
        return result.scalars().all()
    
    async def get_all(self):
        result = await self.db.execute(select(Registration))
        return result.scalars().all()
    
    async def delete_registration(self, registration_id: int):
        registration = await self.db.get(Registration, registration_id)

        if not registration:
            return None

        await self.db.delete(registration)
        await self.db.commit()

        return registration
    

    async def get_by_user_and_event(self, user_id: int, event_id: int):
        result = await self.db.execute(
            select(Registration).where(
                Registration.user_id == user_id,
                Registration.event_id == event_id
            )
        )
        return result.scalar_one_or_none()
    
    async def update_registration(self, registration_id: int, data: dict):
        registration = await self.db.get(Registration, registration_id)

        if not registration:
            return None

        for key, value in data.items():
            setattr(registration, key, value)

        await self.db.commit()
        await self.db.refresh(registration)

        return registration
    
    async def get_user_registrations_with_events(self, user_id: int):
        result = await self.db.execute(
            select(
                Registration.id.label("registration_id"),
                Registration.event_id.label("event_id"),
                Registration.status.label("status"),
                Event.title.label("title"),
                Event.event_date.label("date"),
                Event.location.label("location"),
                Event.image_url.label("image_url"),
            )
            .join(Event, Registration.event_id == Event.id)
            .where(Registration.user_id == user_id)
        )

        rows = result.mappings().all()

        return [
            {
                "registration_id": row["registration_id"],
                "event_id": row["event_id"],
                "status": row["status"],
                "title": row["title"],
                "date": str(row["date"]),
                "location": row["location"],
                "image_url": row["image_url"],
            }
            for row in rows
        ]