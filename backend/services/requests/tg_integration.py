from sqlalchemy import select
from backend.models.tables.feedback import Feedback
from backend.models.tables.user import User

from backend.models.schemas.schemas import (UserSchema, UserResponseSchema, FeedbackSchema)

from typing import List

from backend.models.tables.user_response import UserResponse
from backend.services.conn import connection


@connection
async def get_all_responses(session) -> List[UserResponseSchema]:
    """Get all user responses"""
    result = await session.execute(
        select(UserResponse).order_by(UserResponse.created_at.desc())
    )
    responses = result.scalars().all()
    return [UserResponseSchema.model_validate(r) for r in responses]


@connection
async def get_all_feedbacks(session) -> List[FeedbackSchema]:
    """Get all feedback entries"""
    result = await session.execute(
        select(Feedback).order_by(Feedback.created_at.desc())
    )
    feedbacks = result.scalars().all()
    return [FeedbackSchema.model_validate(f) for f in feedbacks]


@connection
async def set_user(session, tg_id: int, first_name: str = None, username: str = None):
    """Create or get user by Telegram ID"""
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        return UserSchema.model_validate(user)

    new_user = User(tg_id=tg_id, first_name=first_name, username=username)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserSchema.model_validate(new_user)


def get_all_responses(session) -> List[UserResponseSchema]:
    """Get all user responses"""
    result = await session.execute(
        select(UserResponse).order_by(UserResponse.created_at.desc())
    )
    responses = result.scalars().all()
    return [UserResponseSchema.model_validate(r) for r in responses]


@connection
async def get_all_feedbacks(session) -> List[FeedbackSchema]:
    """Get all feedback entries"""
    result = await session.execute(
        select(Feedback).order_by(Feedback.created_at.desc())
    )
    feedbacks = result.scalars().all()
    return [FeedbackSchema.model_validate(f) for f in feedbacks]


@connection
async def set_user(session, tg_id: int, first_name: str = None, username: str = None):
    """Create or get user by Telegram ID"""
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    if user:
        return UserSchema.model_validate(user)

    new_user = User(tg_id=tg_id, first_name=first_name, username=username)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserSchema.model_validate(new_user)
