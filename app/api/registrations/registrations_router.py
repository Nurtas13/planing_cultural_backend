from fastapi import APIRouter
from app.api.registrations.registrations_api import router as registrations_api_router

router = APIRouter()
router.include_router(registrations_api_router)