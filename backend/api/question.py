from fastapi import HTTPException, Path, APIRouter
from typing import List

import backend.services.requests.question as rq
from backend.models.schemas.schemas import (
    QuestionSchema,
    QuestionCreateSchema,
    QuestionUpdateSchema,
)

router = APIRouter(prefix="/api/questions", tags=["Questions"])


@router.post("/", response_model=QuestionSchema, status_code=201)
async def create_question(question_data: QuestionCreateSchema):
    return await rq.create_question(question_data)


@router.get("/", response_model=List[QuestionSchema])
async def get_all_questions():
    return await rq.get_all_questions()


@router.get("/{question_id}", response_model=QuestionSchema)
async def get_question(question_id: int = Path(..., description="Question ID")):
    question = await rq.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.get("/part/{part}", response_model=List[QuestionSchema])
async def get_questions_by_part(part: int = Path(..., ge=1, le=3)):
    return await rq.get_questions_by_part(part)


@router.get("/category/{category}", response_model=List[QuestionSchema])
async def get_questions_by_category(category: str):
    return await rq.get_questions_by_category(category)


@router.get("/difficulty/{difficulty}", response_model=List[QuestionSchema])
async def get_questions_by_difficulty(
    difficulty: str = Path(..., regex="^(Easy|Medium|Hard)$")
):
    return await rq.get_questions_by_difficulty(difficulty)


@router.put("/{question_id}", response_model=QuestionSchema)
async def update_question(
    question_id: int, question_data: QuestionUpdateSchema
):
    question = await rq.update_question(question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/{question_id}")
async def delete_question(question_id: int):
    success = await rq.delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
