from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.models.event import Event


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_events(self):
        result = await self.db.execute(select(Event))
        return result.scalars().all()

    async def get_event_by_id(self, event_id: int):
        result = await self.db.execute(
            select(Event).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def create_event(self, event_data):
        new_event = Event(**event_data.model_dump())
        self.db.add(new_event)
        await self.db.commit()
        await self.db.refresh(new_event)
        return new_event