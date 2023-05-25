from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_models, maker
from app.models import QuizQuestion
from app.network import get_quiz_questions
from app.schemas import Question
from app.crud import check_question, last_question, save_quiz
from app.database import engine

from pydantic import BaseModel

QUIZ_LINK = "https://jservice.io/api/random?count="


class QuestionNum(BaseModel):
    question_num: int

    class Config:
        schema_extra = {
            "example": {
                "question_num": 2,
            }
        }


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def db_connection():
    db = maker()
    try:
        yield db
    finally:
        await db.close()


@app.post("/questions", status_code=201)
async def post_quiz_questions(
    questions_num: QuestionNum, session: AsyncSession = Depends(db_connection)
) -> Question | None:
    if questions_num.question_num <= 0:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="number cannot be less than 1"
        )

    data = await get_quiz_questions(questions_num.question_num, QUIZ_LINK)
    if not data:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="something went wrong with external api",
        )

    last_question_before_import = await last_question(session)

    questions: list[QuizQuestion] = []
    for question in data:
        is_there_question_in_db = await check_question(session, question["id"])
        while is_there_question_in_db:
            question = (await get_quiz_questions(1, QUIZ_LINK))[0]
            is_there_question_in_db = await check_question(session, question["id"])

        q = QuizQuestion(
            id=question["id"],
            question=question["question"],
            answer=question["answer"],
            created_at=question["created_at"],
        )
        questions.append(q)
    await save_quiz(session, questions)
    await session.close()
    return last_question_before_import
