from fastapi import HTTPException, Path

from typing import List
import app.requests as rq
from app.main import app
from app.models.schemas.schemas import (
    UserResponseSchema,
    UserResponseCreateSchema,
    UserResponseUpdateSchema,

)


########################################### User Response Endpoints
@app.post(
    "/api/responses/",
    response_model=UserResponseSchema,
    tags=["Responses"],
    status_code=201,
)
async def create_user_response(response_data: UserResponseCreateSchema):
    return await rq.create_user_response(response_data)


@app.get("/api/responses/", response_model=List[UserResponseSchema], tags=["Responses"])
async def get_all_responses():
    """
    Get all user responses
    """
    return await rq.get_all_responses()


@app.get(
    "/api/responses/{response_id}",
    response_model=UserResponseSchema,
    tags=["Responses"],
)
async def get_user_response(response_id: int = Path(..., description="Response ID")):
    """
    Get user response by ID
    """
    response = await rq.get_user_response(response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@app.get(
    "/api/responses/user/{user_id}",
    response_model=List[UserResponseSchema],
    tags=["Responses"],
)
async def get_user_responses(user_id: int = Path(..., description="User ID")):
    """
    Get all responses for a specific user
    """
    return await rq.get_user_responses(user_id)


@app.get(
    "/api/responses/question/{question_id}",
    response_model=List[UserResponseSchema],
    tags=["Responses"],
)
async def get_responses_by_question(
        question_id: int = Path(..., description="Question ID")
):
    """
    Get all responses for a specific question
    """
    return await rq.get_responses_by_question(question_id)


@app.put(
    "/api/responses/{response_id}",
    response_model=UserResponseSchema,
    tags=["Responses"],
)
async def update_user_response(
        response_id: int = Path(..., description="Response ID"),
        response_data: UserResponseUpdateSchema = None,
):
    """
    Update user response
    """
    response = await rq.update_user_response(response_id, response_data)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@app.delete("/api/responses/{response_id}", tags=["Responses"])
async def delete_user_response(response_id: int = Path(..., description="Response ID")):
    """
    Delete user response by ID
    """
    success = await rq.delete_user_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail="Response not found")
    return {"message": "Response deleted successfully"}
