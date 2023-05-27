from typing import Dict
import httpx
from urllib.parse import urlencode,  urljoin



QUIZ_API_LINK = 'https://jservice.io/api/random'

async def get_quiz_questions(question_num: int) -> list[Dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(QUIZ_API_LINK, params={'count':question_num})
        data: list[Dict[str, str]] = r.json()
        return data

