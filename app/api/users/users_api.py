from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.db.session import get_db
from app.api.users.users_schemas import UserCreate, UserRead
from app.data_access.users.users_repository import UserRepository
from app.business_logic.users.users_service import UserService


router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


@router.get("/users", response_model=list[UserRead])
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/users", response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_data)