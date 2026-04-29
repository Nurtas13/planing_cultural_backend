class EventService:
    def __init__(self, repository):
        self.repository = repository

    async def get_events(self):
        return await self.repository.get_all_events()

    async def get_event(self, event_id: int):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        return event

    async def create_event(self, event_data):
        return await self.repository.create_event(event_data)
    
    async def delete_event(self, event_id: int):
        event = await self.repository.delete_event(event_id)

        if not event:
            raise ValueError("Event not found")

        return event