from fastapi import APIRouter
from app.api.events.events_api import router as events_api_router

router = APIRouter()
router.include_router(events_api_router)