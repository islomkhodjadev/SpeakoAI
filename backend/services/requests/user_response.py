from sqlalchemy import select
from fastapi import HTTPException
from backend.models.tables.question import Question
from backend.models.schemas.schemas import (UserResponseCreateSchema,
                                            UserResponseSchema, UserResponseUpdateSchema
                                            )
from typing import List, Optional

from backend.models.tables.user import User
from backend.models.tables.user_response import UserResponse
from backend.services.conn import connection





# User Response CRUD Operations
@connection
async def create_user_response(session, response_data: UserResponseCreateSchema) -> UserResponseSchema:
    """Create a new user response"""
    try:
        # Verify user and question exist
        user = await session.scalar(select(User).where(User.id == response_data.user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        question = await session.scalar(select(Question).where(Question.id == response_data.question_id))
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        new_response = UserResponse(**response_data.model_dump())
        session.add(new_response)
        await session.commit()
        await session.refresh(new_response)
        return UserResponseSchema.model_validate(new_response)
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating response: {str(e)}")


@connection
async def get_user_response(session, response_id: int) -> Optional[UserResponseSchema]:
    """Get user response by ID"""
    response = await session.scalar(select(UserResponse).where(UserResponse.id == response_id))
    if not response:
        return None
    return UserResponseSchema.model_validate(response)


@connection
async def get_user_responses(session, user_id: int) -> List[UserResponseSchema]:
    """Get all responses for a user"""
    result = await session.execute(
        select(UserResponse).where(UserResponse.user_id == user_id).order_by(UserResponse.created_at.desc())
    )
    responses = result.scalars().all()
    return [UserResponseSchema.model_validate(r) for r in responses]


@connection
async def get_responses_by_question(session, question_id: int) -> List[UserResponseSchema]:
    """Get all responses for a question"""
    result = await session.execute(
        select(UserResponse).where(UserResponse.question_id == question_id).order_by(UserResponse.created_at.desc())
    )
    responses = result.scalars().all()
    return [UserResponseSchema.model_validate(r) for r in responses]


@connection
async def update_user_response(session, response_id: int, response_data: UserResponseUpdateSchema) -> Optional[
    UserResponseSchema]:
    """Update user response by ID"""
    response = await session.scalar(select(UserResponse).where(UserResponse.id == response_id))
    if not response:
        return None

    update_data = response_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(response, field, value)

    await session.commit()
    await session.refresh(response)
    return UserResponseSchema.model_validate(response)


@connection
async def delete_user_response(session, response_id: int) -> bool:
    """Delete user response by ID"""
    response = await session.scalar(select(UserResponse).where(UserResponse.id == response_id))
    if not response:
        return False

    await session.delete(response)
    await session.commit()
    return True
