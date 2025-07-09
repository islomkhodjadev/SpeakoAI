
from backend.core.db.models import Base
from sqlalchemy import ForeignKey, func, String, Float,Text
from sqlalchemy.types import DateTime
from sqlalchemy.orm import  Mapped, mapped_column, relationship
import datetime


class UserResponse(Base):
    __tablename__ = "user_responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    audio_file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    fluency_score: Mapped[float] = mapped_column(Float, nullable=True)
    pronunciation_score: Mapped[float] = mapped_column(Float, nullable=True)
    grammar_score: Mapped[float] = mapped_column(Float, nullable=True)
    vocabulary_score: Mapped[float] = mapped_column(Float, nullable=True)
    overall_score: Mapped[float] = mapped_column(Float, nullable=True)
    ai_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="responses")
    question = relationship("Question", back_populates="responses")
