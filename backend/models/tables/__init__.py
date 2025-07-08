# backend/models/__init__.py
from .user import User
from .feedback import Feedback
from .question import Question
from .user_response import UserResponse
from backend.core.db.models import Base

# This ensures all models are loaded when you import from models
__all__ = ["User", "Feedback", "Question", "UserResponse", "Base"]