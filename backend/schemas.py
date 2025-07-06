from pydantic import BaseModel, ConfigDict
from datetime import datetime


class QuestionSchema(BaseModel):
    id: int
    question: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class UserSchema(BaseModel):
    id: int
    tg_id: int
    first_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


