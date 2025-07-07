from sqlalchemy import select, func, desc
from backend.models  import async_session, User, Question, UserResponse, Feedback

from backend.models.schemas.schemas import (
    QuestionSchema,
    UserScoreSchema, QuestionWithResponsesSchema
)
from typing import List, Optional
from backend.services.conn import connection







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
        average_fluency_score = sum(r.fluency_score for r in scores_with_values if r.fluency_score) / len(
            scores_with_values)
        average_pronunciation_score = sum(
            r.pronunciation_score for r in scores_with_values if r.pronunciation_score) / len(scores_with_values)
        average_grammar_score = sum(r.grammar_score for r in scores_with_values if r.grammar_score) / len(
            scores_with_values)
        average_vocabulary_score = sum(r.vocabulary_score for r in scores_with_values if r.vocabulary_score) / len(
            scores_with_values)
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
