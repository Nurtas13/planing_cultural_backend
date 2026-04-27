from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.models.registration import Registration


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