from sqlalchemy import select, func, desc, and_
from sqlalchemy.orm import selectinload
from models import async_session, User, Question, UserResponse, Feedback
from schemas import (
    QuestionSchema, UserSchema, UserResponseSchema, FeedbackSchema,
    QuestionCreateSchema, UserCreateSchema, UserResponseCreateSchema, FeedbackCreateSchema,
    QuestionUpdateSchema, UserUpdateSchema, UserResponseUpdateSchema, FeedbackUpdateSchema,
    UserScoreSchema, QuestionWithResponsesSchema
)
from typing import List, Optional, Dict, Any
from fastapi import HTTPException


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


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


# Question CRUD Operations
@connection
async def create_question(session, question_data: QuestionCreateSchema) -> QuestionSchema:
    """Create a new question"""
    try:
        new_question = Question(**question_data.model_dump())
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return QuestionSchema.model_validate(new_question)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating question: {str(e)}")


@connection
async def get_question(session, question_id: int) -> Optional[QuestionSchema]:
    """Get question by ID"""
    question = await session.scalar(select(Question).where(Question.id == question_id))
    if not question:
        return None
    return QuestionSchema.model_validate(question)


@connection
async def get_all_questions(session) -> List[QuestionSchema]:
    """Get all questions"""
    result = await session.execute(select(Question).order_by(Question.part, Question.id))
    questions = result.scalars().all()
    return [QuestionSchema.model_validate(q) for q in questions]


@connection
async def get_questions_by_part(session, part: int) -> List[QuestionSchema]:
    """Get questions by IELTS part (1, 2, or 3)"""
    result = await session.execute(select(Question).where(Question.part == part).order_by(Question.id))
    questions = result.scalars().all()
    return [QuestionSchema.model_validate(q) for q in questions]


@connection
async def get_questions_by_category(session, category: str) -> List[QuestionSchema]:
    """Get questions by category"""
    result = await session.execute(select(Question).where(Question.category == category).order_by(Question.id))
    questions = result.scalars().all()
    return [QuestionSchema.model_validate(q) for q in questions]


@connection
async def get_questions_by_difficulty(session, difficulty: str) -> List[QuestionSchema]:
    """Get questions by difficulty level"""
    result = await session.execute(select(Question).where(Question.difficulty == difficulty).order_by(Question.id))
    questions = result.scalars().all()
    return [QuestionSchema.model_validate(q) for q in questions]


@connection
async def update_question(session, question_id: int, question_data: QuestionUpdateSchema) -> Optional[QuestionSchema]:
    """Update question by ID"""
    question = await session.scalar(select(Question).where(Question.id == question_id))
    if not question:
        return None
    
    update_data = question_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)
    
    await session.commit()
    await session.refresh(question)
    return QuestionSchema.model_validate(question)


@connection
async def delete_question(session, question_id: int) -> bool:
    """Delete question by ID"""
    question = await session.scalar(select(Question).where(Question.id == question_id))
    if not question:
        return False
    
    await session.delete(question)
    await session.commit()
    return True


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
async def update_user_response(session, response_id: int, response_data: UserResponseUpdateSchema) -> Optional[UserResponseSchema]:
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


# Feedback CRUD Operations
@connection
async def create_feedback(session, feedback_data: FeedbackCreateSchema) -> FeedbackSchema:
    """Create a new feedback"""
    try:
        # Verify user exists
        user = await session.scalar(select(User).where(User.id == feedback_data.user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        new_feedback = Feedback(**feedback_data.model_dump())
        session.add(new_feedback)
        await session.commit()
        await session.refresh(new_feedback)
        return FeedbackSchema.model_validate(new_feedback)
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating feedback: {str(e)}")


@connection
async def get_feedback(session, feedback_id: int) -> Optional[FeedbackSchema]:
    """Get feedback by ID"""
    feedback = await session.scalar(select(Feedback).where(Feedback.id == feedback_id))
    if not feedback:
        return None
    return FeedbackSchema.model_validate(feedback)


@connection
async def get_user_feedbacks(session, user_id: int) -> List[FeedbackSchema]:
    """Get all feedbacks for a user"""
    result = await session.execute(
        select(Feedback).where(Feedback.user_id == user_id).order_by(Feedback.created_at.desc())
    )
    feedbacks = result.scalars().all()
    return [FeedbackSchema.model_validate(f) for f in feedbacks]


@connection
async def update_feedback(session, feedback_id: int, feedback_data: FeedbackUpdateSchema) -> Optional[FeedbackSchema]:
    """Update feedback by ID"""
    feedback = await session.scalar(select(Feedback).where(Feedback.id == feedback_id))
    if not feedback:
        return None
    
    update_data = feedback_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(feedback, field, value)
    
    await session.commit()
    await session.refresh(feedback)
    return FeedbackSchema.model_validate(feedback)


@connection
async def delete_feedback(session, feedback_id: int) -> bool:
    """Delete feedback by ID"""
    feedback = await session.scalar(select(Feedback).where(Feedback.id == feedback_id))
    if not feedback:
        return False
    
    await session.delete(feedback)
    await session.commit()
    return True


# Analytics and Scoring Operations
@connection
async def get_user_scores(session, user_id: int) -> Optional[UserScoreSchema]:
    """Get comprehensive user scores and statistics"""
    user = await session.scalar(select(User).where(User.id == user_id))
    if not user:
        return None
    
    # Get all responses for the user
    result = await session.execute(
        select(UserResponse).where(UserResponse.user_id == user_id).order_by(UserResponse.created_at.desc())
    )
    responses = result.scalars().all()
    
    if not responses:
        return UserScoreSchema(
            user_id=user_id,
            first_name=user.first_name,
            total_responses=0
        )
    
    # Calculate statistics
    total_responses = len(responses)
    scores_with_values = [r for r in responses if r.overall_score is not None]
    
    if scores_with_values:
        average_overall_score = sum(r.overall_score for r in scores_with_values) / len(scores_with_values)
        average_fluency_score = sum(r.fluency_score for r in scores_with_values if r.fluency_score) / len(scores_with_values)
        average_pronunciation_score = sum(r.pronunciation_score for r in scores_with_values if r.pronunciation_score) / len(scores_with_values)
        average_grammar_score = sum(r.grammar_score for r in scores_with_values if r.grammar_score) / len(scores_with_values)
        average_vocabulary_score = sum(r.vocabulary_score for r in scores_with_values if r.vocabulary_score) / len(scores_with_values)
        best_score = max(r.overall_score for r in scores_with_values)
        recent_scores = [r.overall_score for r in responses[:5] if r.overall_score is not None]
    else:
        average_overall_score = None
        average_fluency_score = None
        average_pronunciation_score = None
        average_grammar_score = None
        average_vocabulary_score = None
        best_score = None
        recent_scores = []
    
    return UserScoreSchema(
        user_id=user_id,
        first_name=user.first_name,
        total_responses=total_responses,
        average_overall_score=average_overall_score,
        average_fluency_score=average_fluency_score,
        average_pronunciation_score=average_pronunciation_score,
        average_grammar_score=average_grammar_score,
        average_vocabulary_score=average_vocabulary_score,
        best_score=best_score,
        recent_scores=recent_scores
    )


@connection
async def get_question_with_responses(session, question_id: int) -> Optional[QuestionWithResponsesSchema]:
    """Get question with all its responses"""
    question = await session.scalar(select(Question).where(Question.id == question_id))
    if not question:
        return None
    
    responses = await get_responses_by_question(session, question_id)
    
    return QuestionWithResponsesSchema(
        question=QuestionSchema.model_validate(question),
        responses=responses,
        total_responses=len(responses)
    )


@connection
async def get_leaderboard(session, limit: int = 10) -> List[UserScoreSchema]:
    """Get leaderboard of users by average score"""
    # Get all users with their average scores
    result = await session.execute(
        select(
            User.id,
            User.first_name,
            func.count(UserResponse.id).label('total_responses'),
            func.avg(UserResponse.overall_score).label('average_score')
        )
        .outerjoin(UserResponse, User.id == UserResponse.user_id)
        .group_by(User.id, User.first_name)
        .having(func.avg(UserResponse.overall_score).isnot(None))
        .order_by(desc(func.avg(UserResponse.overall_score)))
        .limit(limit)
    )
    
    leaderboard = []
    for row in result:
        leaderboard.append(UserScoreSchema(
            user_id=row.id,
            first_name=row.first_name,
            total_responses=row.total_responses,
            average_overall_score=float(row.average_score) if row.average_score else None
        ))
    
    return leaderboard


# Telegram Integration
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
