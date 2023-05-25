from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

from sqlalchemy.sql import functions

class Base(DeclarativeBase):
    pass

class QuizQuestion(Base):
    __tablename__ = "quiz_question"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(800))
    answer: Mapped[str] = mapped_column(String(800))
    created_at: Mapped[datetime] = mapped_column(DateTime)

    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), server_default=functions.now()
    )

    def __repr__(self) -> str:
        return f"""
                QuizQuestion(id={self.id},
                             question={self.question},
                             answer={self.answer},
                             created_at={self.created_at})
                             imported_at={self.imported_at})
                """
