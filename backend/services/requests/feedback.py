
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
