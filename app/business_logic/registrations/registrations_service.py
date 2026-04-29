class RegistrationService:
    def __init__(self, repository):
        self.repository = repository

    async def create_registration(self, registration_data):
        existing_registration = await self.repository.get_by_user_and_event(
            registration_data.user_id,
            registration_data.event_id
        )

        if existing_registration:
            raise ValueError("User is already registered for this event")

        return await self.repository.create_registration(registration_data)

    async def get_user_registrations(self, user_id: int):
        return await self.repository.get_user_registrations_with_events(user_id)

    async def get_all_registrations(self):
        return await self.repository.get_all()

    async def delete_registration(self, registration_id: int):
        registration = await self.repository.delete_registration(registration_id)

        if not registration:
            raise ValueError("Registration not found")

        return registration
    
    async def update_registration(self, registration_id: int, data):
        registration = await self.repository.update_registration(registration_id, data)

        if not registration:
            raise ValueError("Registration not found")

        return registration