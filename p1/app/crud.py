from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.schemas import Question
from app.models import QuizQuestion


async def get_all_questions(session: AsyncSession) -> Sequence[int] | None:
    stmt = select(QuizQuestion.id).where(QuizQuestion.id > 0)
    ret_list = []
    async with session.begin():
        ret_list = (await session.scalars(stmt)).all()
    return ret_list


async def save_quiz(session: AsyncSession, data: list[dict]):
    stmt = pg_insert(QuizQuestion).values(data)
    async with session.begin():
        ids = await session.execute(stmt)
    return ids


async def last_question(session: AsyncSession) -> Question | None:
    stmt = select(QuizQuestion).order_by(QuizQuestion.imported_at.desc()).limit(1)
    async with session.begin():
        q = (await session.scalars(stmt)).one_or_none()
        if q is None:
            return None
        return Question(
            id=q.id, question=q.question, answer=q.answer, created_at=q.created_at
        )
