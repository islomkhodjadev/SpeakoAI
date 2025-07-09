from fastapi import HTTPException, Path, APIRouter
from typing import List

import backend.services.requests.user_response as rq
from backend.models.schemas.schemas import (
    UserResponseSchema,
    UserResponseCreateSchema,
    UserResponseUpdateSchema,
)

router = APIRouter(prefix="/api/responses", tags=["Responses"])


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user_response(response_data: UserResponseCreateSchema):
    return await rq.create_user_response(response_data)


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_responses():
    return await rq.get_all_responses()


@router.get("/{response_id}", response_model=UserResponseSchema)
async def get_user_response(response_id: int = Path(...)):
    response = await rq.get_user_response(response_id)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@router.get("/user/{user_id}", response_model=List[UserResponseSchema])
async def get_user_responses(user_id: int = Path(...)):
    return await rq.get_user_responses(user_id)


@router.get("/question/{question_id}", response_model=List[UserResponseSchema])
async def get_responses_by_question(question_id: int = Path(...)):
    return await rq.get_responses_by_question(question_id)


@router.put("/{response_id}", response_model=UserResponseSchema)
async def update_user_response(
    response_id: int = Path(...),
    response_data: UserResponseUpdateSchema = None,
):
    response = await rq.update_user_response(response_id, response_data)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@router.delete("/{response_id}")
async def delete_user_response(response_id: int = Path(...)):
    success = await rq.delete_user_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail="Response not found")
    return {"message": "Response deleted successfully"}
