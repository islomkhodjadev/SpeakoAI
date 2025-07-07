from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models import init_db
from backend.services import requests as rq
import uvicorn
from app.models.schemas.schemas import (
    UserSchema,
)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("SpeakoAI API is ready!")
    yield


app = FastAPI(
    title="SpeakoAI - IELTS Speaking Practice API",
    description="""
    A comprehensive API for IELTS speaking practice with AI-powered scoring and feedback.
    """,
    version="1.0.0",
    contact={
        "name": "SpeakoAI Support",
        "email": "support@speakoai.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Health check
@app.get("/", tags=["Health"])
async def root():
    return {"message": "SpeakoAI API is running!", "status": "healthy"}




# Telegram Integration Endpoints
@app.post(
    "/api/telegram/user", response_model=UserSchema, tags=["Telegram Integration"]
)
async def create_telegram_user(
    tg_id: int = Query(..., description="Telegram user ID"),
    first_name: str = Query(..., description="User's first name"),
    username: Optional[str] = Query(None, description="Telegram username"),
):
    """
    Create or get user from Telegram data
    """
    return await rq.set_user(tg_id, first_name, username)






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
