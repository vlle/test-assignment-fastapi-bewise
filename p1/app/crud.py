from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import Question
from app.models import QuizQuestion

from datetime import datetime


async def save_quiz(
    session: AsyncSession, data: list[dict[str, (int | str | datetime)]]
) -> int:
    stmt = (
        pg_insert(QuizQuestion)
        .on_conflict_do_nothing(index_elements=[QuizQuestion.id])
        .values(data)
    )
    stmt = stmt.returning(QuizQuestion.id)
    async with session.begin():
        result = (await session.execute(stmt)).all()
    return len(result)


async def last_question(session: AsyncSession) -> Question | None:
    stmt = select(QuizQuestion).order_by(QuizQuestion.imported_at.desc()).limit(1)
    async with session.begin():
        q = (await session.scalars(stmt)).one_or_none()
        if q is None:
            return None
        return Question(
            id=q.id, question=q.question, answer=q.answer, created_at=q.created_at
        )
