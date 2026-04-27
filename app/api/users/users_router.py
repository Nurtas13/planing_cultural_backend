from fastapi import APIRouter
from app.api.users.users_api import router as users_api_router

router = APIRouter()
router.include_router(users_api_router)