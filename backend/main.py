from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from models import init_db
import requests as rq
import uvicorn
from schemas import (
    QuestionSchema,
    UserSchema,
    UserResponseSchema,
    FeedbackSchema,
    QuestionCreateSchema,
    UserCreateSchema,
    UserResponseCreateSchema,
    FeedbackCreateSchema,
    QuestionUpdateSchema,
    UserUpdateSchema,
    UserResponseUpdateSchema,
    FeedbackUpdateSchema,
    UserScoreSchema,
    QuestionWithResponsesSchema,
)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print("SpeakoAI API is ready!")
    yield


app = FastAPI(
    title="SpeakoAI - IELTS Speaking Practice API",
    description="""
    A comprehensive API for IELTS speaking practice with AI-powered scoring and feedback.
    
    ## Features
    * **IELTS Speaking Questions**: Questions for all 3 parts with sample answers
    * **User Management**: Telegram user integration and profile management
    * **Response Tracking**: Record and analyze user speaking responses
    * **AI Scoring**: Automated scoring for fluency, pronunciation, grammar, and vocabulary
    * **Feedback System**: AI-generated feedback for improvement
    * **Analytics**: User progress tracking and leaderboards
    
    ## IELTS Speaking Parts
    * **Part 1**: Personal information and familiar topics (4-5 minutes)
    * **Part 2**: Individual long turn with cue card (3-4 minutes)
    * **Part 3**: Two-way discussion on abstract topics (4-5 minutes)
    """,
    version="1.0.0",
    contact={
        "name": "SpeakoAI Support",
        "email": "support@speakoai.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code},
    )


# Health check
@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint
    """
    return {"message": "SpeakoAI API is running!", "status": "healthy"}


# User Endpoints
@app.post("/api/users/", response_model=UserSchema, tags=["Users"], status_code=201)
async def create_user(user_data: UserCreateSchema):
    """
    Create a new user

    - **tg_id**: Telegram user ID (required)
    - **first_name**: User's first name (required)
    - **username**: Telegram username (optional)
    """
    return await rq.create_user(user_data)


@app.get("/api/users/", response_model=List[UserSchema], tags=["Users"])
async def get_all_users():
    """
    Get all users in the system
    """
    return await rq.get_all_users()


@app.get("/api/users/{tg_id}", response_model=UserSchema, tags=["Users"])
async def get_user(tg_id: int = Path(..., description="Telegram user ID")):
    """
    Get user by Telegram ID
    """
    user = await rq.get_user(tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/users/{tg_id}", response_model=UserSchema, tags=["Users"])
async def update_user(
    tg_id: int = Path(..., description="Telegram user ID"),
    user_data: UserUpdateSchema = None,
):
    """
    Update user information
    """
    user = await rq.update_user(tg_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/api/users/{tg_id}", tags=["Users"])
async def delete_user(tg_id: int = Path(..., description="Telegram user ID")):
    """
    Delete user by Telegram ID
    """
    success = await rq.delete_user(tg_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


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
    - **category**: Question category (e.g., "Family", "Work")
    - **difficulty**: Difficulty level ("Easy", "Medium", "Hard")
    """
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


# User Response Endpoints
@app.post(
    "/api/responses/",
    response_model=UserResponseSchema,
    tags=["Responses"],
    status_code=201,
)
async def create_user_response(response_data: UserResponseCreateSchema):
    """
    Create a new user response to an IELTS question

    - **user_id**: User ID
    - **question_id**: Question ID
    - **response_text**: User's response text
    - **audio_file_path**: Optional path to audio file
    - **fluency_score**: Fluency score (0-9)
    - **pronunciation_score**: Pronunciation score (0-9)
    - **grammar_score**: Grammar score (0-9)
    - **vocabulary_score**: Vocabulary score (0-9)
    - **overall_score**: Overall score (0-9)
    - **ai_feedback**: AI-generated feedback
    """
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


# Feedback Endpoints
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


# Analytics Endpoints
@app.get(
    "/api/analytics/user/{user_id}", response_model=UserScoreSchema, tags=["Analytics"]
)
async def get_user_analytics(user_id: int = Path(..., description="User ID")):
    """
    Get comprehensive analytics for a user including scores and progress
    """
    analytics = await rq.get_user_scores(user_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="User not found")
    return analytics


@app.get(
    "/api/analytics/leaderboard",
    response_model=List[UserScoreSchema],
    tags=["Analytics"],
)
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100, description="Number of top users to return")
):
    """
    Get leaderboard of users ranked by average score
    """
    return await rq.get_leaderboard(limit)


@app.get(
    "/api/analytics/question/{question_id}",
    response_model=QuestionWithResponsesSchema,
    tags=["Analytics"],
)
async def get_question_analytics(
    question_id: int = Path(..., description="Question ID")
):
    """
    Get question with all its responses for analytics
    """
    analytics = await rq.get_question_with_responses(question_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Question not found")
    return analytics


# Telegram Integration Endpoints
@app.post(
    "/api/telegram/user", response_model=UserSchema, tags=["Telegram Integration"]
)
async def create_telegram_user(
    tg_id: int = Query(..., description="Telegram user ID"),
    first_name: str = Query(..., description="User's first name"),
    username: Optional[str] = Query(None, description="Telegram username"),
):
    """
    Create or get user from Telegram data
    """
    return await rq.set_user(tg_id, first_name, username)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
