from fastapi import  HTTPException, Path

from typing import List
import app.requests as rq
from app.models.schemas.schemas import (
    QuestionSchema,
    QuestionCreateSchema,
    QuestionUpdateSchema,

)

from app.main import app


# Question Endpoints
@app.post(
    "/api/questions/",
    response_model=QuestionSchema,
    tags=["Questions"],
    status_code=201,
)
async def create_question(question_data: QuestionCreateSchema):
    """
    Create a new IELTS speaking question

    - **part**: IELTS speaking part (1, 2, or 3)
    - **question_text**: The question text
    - **sample_answer**: Optional sample answer
    - **category**: Question category (e.g., "Family", "Work")"""
    return await rq.create_question(question_data)


@app.get("/api/questions/", response_model=List[QuestionSchema], tags=["Questions"])
async def get_all_questions():
    """
    Get all IELTS speaking questions
    """
    return await rq.get_all_questions()


@app.get(
    "/api/questions/{question_id}", response_model=QuestionSchema, tags=["Questions"]
)
async def get_question(question_id: int = Path(..., description="Question ID")):
    """
    Get question by ID
    """
    question = await rq.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.get(
    "/api/questions/part/{part}",
    response_model=List[QuestionSchema],
    tags=["Questions"],
)
async def get_questions_by_part(
        part: int = Path(..., ge=1, le=3, description="IELTS speaking part")
):
    """
    Get questions by IELTS speaking part (1, 2, or 3)
    """
    return await rq.get_questions_by_part(part)


@app.get(
    "/api/questions/category/{category}",
    response_model=List[QuestionSchema],
    tags=["Questions"],
)
async def get_questions_by_category(
        category: str = Path(..., description="Question category")
):
    """
    Get questions by category
    """
    return await rq.get_questions_by_category(category)


@app.get(
    "/api/questions/difficulty/{difficulty}",
    response_model=List[QuestionSchema],
    tags=["Questions"],
)
async def get_questions_by_difficulty(
        difficulty: str = Path(
            ..., regex="^(Easy|Medium|Hard)$", description="Difficulty level"
        )
):
    """
    Get questions by difficulty level
    """
    return await rq.get_questions_by_difficulty(difficulty)


@app.put(
    "/api/questions/{question_id}", response_model=QuestionSchema, tags=["Questions"]
)
async def update_question(
        question_id: int = Path(..., description="Question ID"),
        question_data: QuestionUpdateSchema = None,
):
    """
    Update question
    """
    question = await rq.update_question(question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.delete("/api/questions/{question_id}", tags=["Questions"])
async def delete_question(question_id: int = Path(..., description="Question ID")):
    """
    Delete question by ID
    """
    success = await rq.delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
