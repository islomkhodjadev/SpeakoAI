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
