from typing import Dict
import httpx

async def get_quiz_questions(question_num: int,
                             quiz_link: str) -> list[Dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(quiz_link + str(
            question_num))
        data: list[Dict] = r.json()
        return data

