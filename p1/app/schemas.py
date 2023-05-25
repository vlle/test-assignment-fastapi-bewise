from datetime import datetime
from pydantic import BaseModel

class Question(BaseModel):
    id: int | None = None
    question: str | None = None
    answer: str | None = None
    created_at: datetime | None = None

