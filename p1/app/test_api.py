import pytest
import app.test_variable
from app.database import engine, init_models
from main import app
from fastapi.testclient import TestClient
from fastapi import status

@pytest.fixture()
async def model_load():
    await init_models(engine)

@pytest.fixture()
def client():
    client = TestClient(app)
    return client

def test_post_minus_quiz(client):
    response = client.post("/questions", json={'question_num':'-1'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_is_last_question_stored(client, model_load):
    await model_load
    question = None
    response = client.post("/questions", json={'question_num':'1'})
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data == question

    question = data
    response = client.post("/questions", json={'question_num':'1'})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != question
    assert response.json() is not None
