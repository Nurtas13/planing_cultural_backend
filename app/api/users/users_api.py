from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.data_access.db.session import get_db
from app.api.users.users_schemas import (
    UserCreate,
    UserRead,
    UserLogin,
    UserUpdate,
    UserDelete,
    GoogleLogin,
)
from app.data_access.users.users_repository import UserRepository
from app.business_logic.users.users_service import UserService


router = APIRouter()

SECRET_KEY = "planning-cultural-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


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
    try:
        return await service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_user(
    login_data: UserLogin,
    service: UserService = Depends(get_user_service)
):
    try:
        user = await service.login_user(login_data)

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/google-login")
async def google_login(
    google_data: GoogleLogin,
    service: UserService = Depends(get_user_service)
):
    try:
        user = await service.google_login(google_data)

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    try:
        return await service.update_user(user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/users/delete-account")
async def delete_account(
    delete_data: UserDelete,
    service: UserService = Depends(get_user_service)
):
    try:
        await service.delete_user_by_email(delete_data)
        return {"message": "Account deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))