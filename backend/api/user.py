import app.requests as rq
from app.models.schemas.schemas import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from fastapi import HTTPException, Path
from typing import List
from app.main import app



# User Endpoints
@app.post("/api/users/", response_model=UserSchema, tags=["Users"], status_code=201)
async def create_user(user_data: UserCreateSchema):
    """
    Create a new user

    - **tg_id**: Telegram user ID (required)
    - **first_name**: User's first name (required)
    - **username**: Telegram username (optional)
    """
    return await rq.create_user(user_data)


@app.get("/api/users/", response_model=List[UserSchema], tags=["Users"])
async def get_all_users():
    """
    Get all users in the system
    """
    return await rq.get_all_users()


@app.get("/api/users/{tg_id}", response_model=UserSchema, tags=["Users"])
async def get_user(tg_id: int = Path(..., description="Telegram user ID")):
    """
    Get user by Telegram ID
    """
    user = await rq.get_user(tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/users/{tg_id}", response_model=UserSchema, tags=["Users"])
async def update_user(
        tg_id: int = Path(..., description="Telegram user ID"),
        user_data: UserUpdateSchema = None,
):
    """
    Update user information
    """
    user = await rq.update_user(tg_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/api/users/{tg_id}", tags=["Users"])
async def delete_user(tg_id: int = Path(..., description="Telegram user ID")):
    """
    Delete user by Telegram ID
    """
    success = await rq.delete_user(tg_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
