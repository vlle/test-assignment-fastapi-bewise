from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_models, maker
from app.network import get_quiz_questions
from httpx import ReadTimeout
from app.crud import last_question, save_quiz, get_all_questions
from app.database import engine
from app.schemas import Question

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


unique_questions = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models(engine)
    async with AsyncSession(engine) as session:
        questions_from_db = await get_all_questions(session)
    if questions_from_db:
        for q in questions_from_db:
            unique_questions.add(q)
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

    try:
        data = await get_quiz_questions(questions_num.question_num, QUIZ_LINK)
        if not data:
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

    # external api limitation
    if questions_num.question_num > 100:
        questions_num.question_num = 100
    converted_data = []
    current_len = 0
    while current_len < questions_num.question_num:
        for d in data:
            try:
                if d["id"] not in unique_questions:
                    item = {
                        "id": d["id"],
                        "answer": d["answer"],
                        "question": d["question"],
                        "created_at": d["created_at"],
                    }
                    converted_data.append(item)
                    unique_questions.add(d["question"])
                    current_len += 1
            except TypeError:
                break
        if current_len < questions_num.question_num:
            # we will ask for more questions to reduce number of external api calls
            try:
                data = await get_quiz_questions(
                    questions_num.question_num - current_len * 2, QUIZ_LINK
                )
                # external api may return string error or refuse to give data
                if not data or isinstance(data, str):
                    break
            except ReadTimeout:
                break

    await save_quiz(session, converted_data)
    return last_question_before_import
