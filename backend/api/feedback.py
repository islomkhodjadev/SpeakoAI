from fastapi import HTTPException, Path, APIRouter
from typing import List

import backend.services.requests.feedback as rq
from backend.models.schemas.schemas import (
    FeedbackSchema,
    FeedbackCreateSchema,
    FeedbackUpdateSchema,
)

router = APIRouter(prefix="/api/feedbacks", tags=["Feedbacks"])


@router.post("/", response_model=FeedbackSchema, status_code=201)
async def create_feedback(feedback_data: FeedbackCreateSchema):
    return await rq.create_feedback(feedback_data)


@router.get("/", response_model=List[FeedbackSchema])
async def get_all_feedbacks():
    return await rq.get_all_feedbacks()


@router.get("/{feedback_id}", response_model=FeedbackSchema)
async def get_feedback(feedback_id: int = Path(..., description="Feedback ID")):
    feedback = await rq.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.get("/user/{user_id}", response_model=List[FeedbackSchema])
async def get_user_feedbacks(user_id: int = Path(..., description="User ID")):
    return await rq.get_user_feedbacks(user_id)


@router.put("/{feedback_id}", response_model=FeedbackSchema)
async def update_feedback(
    feedback_id: int = Path(..., description="Feedback ID"),
    feedback_data: FeedbackUpdateSchema = None,
):
    feedback = await rq.update_feedback(feedback_id, feedback_data)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: int = Path(..., description="Feedback ID")):
    success = await rq.delete_feedback(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}
