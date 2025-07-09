from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional
import uvicorn
from backend.core.db.models import init_db
from backend.services import requests as rq
from backend.models.schemas.schemas import UserSchema
from backend.api import feedback, user, question, user_response, error_handle


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("SpeakoAI API is ready!")
    yield


app = FastAPI(
    title="SpeakoAI - IELTS Speaking Practice API",
    description="A comprehensive API for IELTS speaking practice with AI-powered scoring and feedback.",
    version="1.0.0",
    contact={"name": "SpeakoAI Support", "email": "support@speakoai.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "SpeakoAI API is running!", "status": "healthy"}


app.include_router(feedback.router)
app.include_router(user.router)
app.include_router(question.router)
app.include_router(user_response.router)
app.add_exception_handler(RequestValidationError, error_handle.http_exception_handler)


@app.post("/api/telegram/user", response_model=UserSchema, tags=["Telegram Integration"])
async def create_telegram_user(
        tg_id: int = Query(..., description="Telegram user ID"),
        first_name: str = Query(..., description="User's first name"),
        username: Optional[str] = Query(None, description="Telegram username"),
):
    return await rq.set_user(tg_id, first_name, username)


# --- MAIN ---
if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
