from fastapi import APIRouter, HTTPException, Path
from typing import List

import backend.services.requests.user as rq
from backend.models.schemas.schemas import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/", response_model=UserSchema, status_code=201)
async def create_user(user_data: UserCreateSchema):
    return await rq.create_user(user_data)


@router.get("/", response_model=List[UserSchema])
async def get_all_users():
    return await rq.get_all_users()


@router.get("/{tg_id}", response_model=UserSchema)
async def get_user(tg_id: int = Path(..., description="Telegram user ID")):
    user = await rq.get_user(tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{tg_id}", response_model=UserSchema)
async def update_user(
    tg_id: int = Path(..., description="Telegram user ID"),
    user_data: UserUpdateSchema = None,
):
    user = await rq.update_user(tg_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{tg_id}")
async def delete_user(tg_id: int = Path(..., description="Telegram user ID")):
    success = await rq.delete_user(tg_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
