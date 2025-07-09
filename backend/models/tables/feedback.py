
from backend.core.db.models import Base
from sqlalchemy import  ForeignKey, func, Text
from sqlalchemy.types import DateTime
from sqlalchemy.orm import  Mapped, mapped_column, relationship
import datetime


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ai_comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="feedbacks")
