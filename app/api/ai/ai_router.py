from fastapi import APIRouter
from app.api.ai.ai_api import router as ai_api_router


router = APIRouter()
router.include_router(ai_api_router)