from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import  List
from models import init_db
from schemas import QuestionSchema, UserSchema
import requests as rq
import uvicorn


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("bot is ready")


app = FastAPI(title="SpeakoAI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/all_questions/", response_model=List[QuestionSchema])
async def all_questions():
    res =await rq.get_all_questions()
    return res

@app.get("/api/user/{tg_id}", response_model=List[UserSchema])
async def get_user(tg_id:int):
    user =await rq.get_user(tg_id=tg_id)
    if not user:
        return None

    return user

