from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import Question
from app.models import QuizQuestion


async def save_quiz(session: AsyncSession, quiz: list[QuizQuestion]) -> None:
    async with session.begin():
        session.add_all(quiz)

async def last_question(session: AsyncSession) -> Question | None:
    stmt = (
            select(QuizQuestion).order_by(QuizQuestion.imported_at.desc()).limit(1)
            )
    async with session.begin():
        q = (await session.scalars(stmt)).one_or_none()
        if q is None:
            return None
        return Question(id=q.id,
                        question=q.question,
                        answer=q.answer,
                        created_at=q.created_at)

async def check_question(session: AsyncSession, id: int) -> bool:
    async with session.begin():
        q = await session.get(QuizQuestion, id)
        return q is not None
