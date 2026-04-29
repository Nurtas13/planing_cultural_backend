from fastapi import APIRouter, HTTPException
from openai import OpenAI

from app.core.config import settings
from app.api.ai.ai_schemas import AIRequest, AIResponse


router = APIRouter()

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@router.post("/ai", response_model=AIResponse)
def ask_ai(data: AIRequest):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"""
Ты помощник мобильного приложения для планирования культурных событий.
Отвечай кратко, понятно и по теме.

Вопрос пользователя:
{data.message}
"""
        )

        return AIResponse(answer=response.output_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))