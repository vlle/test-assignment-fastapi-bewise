from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from httpx import ReadTimeout
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_models, maker, engine
from app.network import get_quiz_questions
from app.crud import last_question, save_quiz, get_all_questions
from app.schemas import Question

from pydantic import BaseModel, Field


class QuestionNum(BaseModel):
    question_num: int = Field(..., gt=0, lt=101)

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
):
    try:
        questions = await get_quiz_questions(questions_num.question_num)
        if not questions:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="something went wrong with external api",
            )
    except ReadTimeout:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="something went wrong with external api",
        )

    last_question_before_import = await last_question(session)

    inserted_ids = 0
    while inserted_ids < questions_num.question_num:
        inserted_ids += await save_quiz(session, questions)
        count_conflicts = questions_num.question_num - inserted_ids
        print(count_conflicts)
        if count_conflicts > 0:
            questions = await get_quiz_questions(count_conflicts)
    return last_question_before_import
