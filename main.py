from app.data_access.db.base import Base
from app.data_access.db.session import engine

from app.data_access.models.user import User
from app.data_access.models.event import Event
from app.data_access.models.registration import Registration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_router import api_router

from dotenv import load_dotenv
import os

load_dotenv()

print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Cultural Events Planning API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(api_router)