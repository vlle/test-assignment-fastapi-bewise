from typing import Dict
import httpx


QUIZ_API_LINK = "https://jservice.io/api/random"


async def get_quiz_questions(question_num: int) -> list[Dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(QUIZ_API_LINK, params={"count": question_num})
        r.raise_for_status()

        questions: list[Dict[str, str]] = r.json()
    return [
        {
            "id": d["id"],
            "answer": d["answer"],
            "question": d["question"],
            "created_at": d["created_at"],
        }
        for d in questions
    ]
