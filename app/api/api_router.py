from fastapi import APIRouter

from app.api.users.users_router import router as users_router
from app.api.events.events_router import router as events_router
from app.api.registrations.registrations_router import router as registrations_router


api_router = APIRouter()

api_router.include_router(users_router, tags=["Users"])
api_router.include_router(events_router, tags=["Events"])
api_router.include_router(registrations_router, tags=["Registrations"])