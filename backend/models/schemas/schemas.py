from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List


class QuestionSchema(BaseModel):
    id: int
    part: int = Field(..., ge=1, le=3, description="IELTS speaking part (1, 2, or 3)")
    question_text: str
    sample_answer: Optional[str] = None
    category: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionCreateSchema(BaseModel):
    part: int = Field(..., ge=1, le=3, description="IELTS speaking part (1, 2, or 3)")
    question_text: str = Field(..., min_length=10, description="The question text")
    sample_answer: Optional[str] = None
    category: Optional[str] = None


class QuestionUpdateSchema(BaseModel):
    part: Optional[int] = Field(None, ge=1, le=3)
    question_text: Optional[str] = Field(None, min_length=10)
    sample_answer: Optional[str] = None
    category: Optional[str] = None


class UserSchema(BaseModel):
    id: int
    tg_id: int
    first_name: str
    username: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    tg_id: int = Field(..., description="Telegram user ID")
    first_name: str = Field(..., min_length=1, max_length=25)
    username: Optional[str] = Field(None, max_length=50)


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=25)
    username: Optional[str] = Field(None, max_length=50)


class UserResponseSchema(BaseModel):
    id: int
    user_id: int
    question_id: int
    response_text: str
    audio_file_path: Optional[str] = None
    fluency_score: Optional[float] = Field(None, ge=0, le=9)
    pronunciation_score: Optional[float] = Field(None, ge=0, le=9)
    grammar_score: Optional[float] = Field(None, ge=0, le=9)
    vocabulary_score: Optional[float] = Field(None, ge=0, le=9)
    overall_score: Optional[float] = Field(None, ge=0, le=9)
    ai_feedback: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserResponseCreateSchema(BaseModel):
    user_id: int
    question_id: int
    response_text: str = Field(..., min_length=10)
    audio_file_path: Optional[str] = None
    fluency_score: Optional[float] = Field(None, ge=0, le=9)
    pronunciation_score: Optional[float] = Field(None, ge=0, le=9)
    grammar_score: Optional[float] = Field(None, ge=0, le=9)
    vocabulary_score: Optional[float] = Field(None, ge=0, le=9)
    overall_score: Optional[float] = Field(None, ge=0, le=9)
    ai_feedback: Optional[str] = None


class UserResponseUpdateSchema(BaseModel):
    response_text: Optional[str] = Field(None, min_length=10)
    audio_file_path: Optional[str] = None
    fluency_score: Optional[float] = Field(None, ge=0, le=9)
    pronunciation_score: Optional[float] = Field(None, ge=0, le=9)
    grammar_score: Optional[float] = Field(None, ge=0, le=9)
    vocabulary_score: Optional[float] = Field(None, ge=0, le=9)
    overall_score: Optional[float] = Field(None, ge=0, le=9)
    ai_feedback: Optional[str] = None


class FeedbackSchema(BaseModel):
    id: int
    user_id: int
    ai_comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FeedbackCreateSchema(BaseModel):
    user_id: int
    ai_comment: str = Field(..., min_length=10)


class FeedbackUpdateSchema(BaseModel):
    ai_comment: str = Field(..., min_length=10)


class UserScoreSchema(BaseModel):
    user_id: int
    first_name: str
    total_responses: int
    average_overall_score: Optional[float] = None
    average_fluency_score: Optional[float] = None
    average_pronunciation_score: Optional[float] = None
    average_grammar_score: Optional[float] = None
    average_vocabulary_score: Optional[float] = None
    best_score: Optional[float] = None
    recent_scores: List[float] = []


class QuestionWithResponsesSchema(BaseModel):
    question: QuestionSchema
    responses: List[UserResponseSchema] = []
    total_responses: int = 0


