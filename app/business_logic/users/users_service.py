class UserService:
    def __init__(self, repository):
        self.repository = repository

    async def get_users(self):
        return await self.repository.get_all_users()

    async def get_user(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def create_user(self, user_data):
        return await self.repository.create_user(user_data)