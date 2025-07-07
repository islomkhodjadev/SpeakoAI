

from fastapi import  HTTPException, Path
from typing import List
import app.requests as rq
from app.models.schemas.schemas import (
    FeedbackSchema,
    FeedbackCreateSchema,
    FeedbackUpdateSchema,
)
from app.main import app







############################################ Feedback Endpoints
@app.post(
    "/api/feedbacks/",
    response_model=FeedbackSchema,
    tags=["Feedbacks"],
    status_code=201,
)
async def create_feedback(feedback_data: FeedbackCreateSchema):
    """
    Create a new feedback entry

    - **user_id**: User ID
    - **ai_comment**: AI-generated feedback comment
    """
    return await rq.create_feedback(feedback_data)


@app.get("/api/feedbacks/", response_model=List[FeedbackSchema], tags=["Feedbacks"])
async def get_all_feedbacks():
    """
    Get all feedback entries
    """
    return await rq.get_all_feedbacks()


@app.get(
    "/api/feedbacks/{feedback_id}", response_model=FeedbackSchema, tags=["Feedbacks"]
)
async def get_feedback(feedback_id: int = Path(..., description="Feedback ID")):
    """
    Get feedback by ID
    """
    feedback = await rq.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@app.get(
    "/api/feedbacks/user/{user_id}",
    response_model=List[FeedbackSchema],
    tags=["Feedbacks"],
)
async def get_user_feedbacks(user_id: int = Path(..., description="User ID")):
    """
    Get all feedback for a specific user
    """
    return await rq.get_user_feedbacks(user_id)


@app.put(
    "/api/feedbacks/{feedback_id}", response_model=FeedbackSchema, tags=["Feedbacks"]
)
async def update_feedback(
    feedback_id: int = Path(..., description="Feedback ID"),
    feedback_data: FeedbackUpdateSchema = None,
):
    """
    Update feedback
    """
    feedback = await rq.update_feedback(feedback_id, feedback_data)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@app.delete("/api/feedbacks/{feedback_id}", tags=["Feedbacks"])
async def delete_feedback(feedback_id: int = Path(..., description="Feedback ID")):
    """
    Delete feedback by ID
    """
    success = await rq.delete_feedback(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}

