from sqlalchemy import select
from fastapi import HTTPException
from backend.models.schemas.schemas import (
 UserCreateSchema,
    UserSchema, UserUpdateSchema
)
from typing import List, Optional

from backend.models.tables.user import User
from backend.services.conn import connection



# User CRUD Operations
@connection
async def create_user(session, user_data: UserCreateSchema) -> UserSchema:
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = await session.scalar(select(User).where(User.tg_id == user_data.tg_id))
        if existing_user:
            return UserSchema.model_validate(existing_user)

        new_user = User(**user_data.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserSchema.model_validate(new_user)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


@connection
async def get_user(session, tg_id: int) -> Optional[UserSchema]:
    """Get user by Telegram ID"""
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return None
    return UserSchema.model_validate(user)


@connection
async def get_user_by_id(session, user_id: int) -> Optional[UserSchema]:
    """Get user by internal ID"""
    user = await session.scalar(select(User).where(User.id == user_id))
    if not user:
        return None
    return UserSchema.model_validate(user)


@connection
async def get_all_users(session) -> List[UserSchema]:
    """Get all users"""
    result = await session.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [UserSchema.model_validate(user) for user in users]


@connection
async def update_user(session, tg_id: int, user_data: UserUpdateSchema) -> Optional[UserSchema]:
    """Update user by Telegram ID"""
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return UserSchema.model_validate(user)


@connection
async def delete_user(session, tg_id: int) -> bool:
    """Delete user by Telegram ID"""
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True

