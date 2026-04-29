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
        existing_user = await self.repository.get_user_by_email(user_data.email)

        if existing_user:
            raise ValueError("User with this email already exists")

        data = user_data.model_dump()
        password = data.pop("password")
        data["password_hash"] = password

        return await self.repository.create_user_from_dict(data)

    async def login_user(self, login_data):
        user = await self.repository.get_user_by_email(login_data.email)

        if not user or user.password_hash != login_data.password:
            raise ValueError("Invalid email or password")

        return user

    async def update_user(self, user_id: int, data):
        user = await self.repository.update_user(
            user_id,
            data.model_dump(exclude_unset=True)
        )

        if not user:
            raise ValueError("User not found")

        return user