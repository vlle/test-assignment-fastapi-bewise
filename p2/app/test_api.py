import uuid
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

@pytest.mark.asyncio
async def test_is_user_registered(client: TestClient, model_load):
    await model_load
    response = client.post("/user", json={'nick':'ivan'})
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_is_audio_saved(client: TestClient, model_load):
    await model_load
    response = client.post("/user", json={'nick':'ivan'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    with open("audio-samples/sample1.wav","rb") as f:
        file_bytes = f.read()
    files = {"file": ("testfile.wav", file_bytes)}
    response = client.post("/audio",
                           data={'id':data["id"],
                                 'uuid':data["uuid"]},
                           files=files)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_is_audio_downloaded(client: TestClient, model_load):
    await model_load
    response = client.post("/user", json={'nick':'ivan'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    with open("audio-samples/sample1.wav","rb") as f:
        file_bytes = f.read()
    files = {"file": ("testfile.wav", file_bytes)}
    response = client.post("/audio",
                            data={'id':data["id"],
                                'uuid':data["uuid"]},
                           files=files)
    data = response.json()
    link = data["link"]
    response = client.get(link)
    assert response.headers["content-type"] == "audio/mpeg"

@pytest.mark.asyncio
async def test_is_audio_access_validated(client: TestClient, model_load):
    await model_load
    response = client.post("/user", json={'nick':'ivan'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    with open("audio-samples/sample1.wav","rb") as f:
        file_bytes = f.read()
    files = {"file": ("testfile.wav", file_bytes)}
    response = client.post("/audio",
                           data={'id':data["id"],
                                 'uuid':data["uuid"]},
                           files=files)
    data = response.json()
    link = data["link"]

    wrong_user_id_link = link + '3'
    response = client.get(wrong_user_id_link)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    wrong_format_id_link = link + 'wrong'
    response = client.get(wrong_format_id_link)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_is_user_and_uuid_validated(client: TestClient, model_load):
    await model_load
    response = client.post("/user", json={'nick':'ivan'})
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    with open("audio-samples/sample1.wav","rb") as f:
        file_bytes = f.read()
    files = {"file": ("testfile.wav", file_bytes)}

    response = client.post("/audio",
                           data={'id':data["id"]+1,
                                 'uuid':data["uuid"]},
                           files=files)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    wrong_uuid = str(uuid.uuid4())
    response = client.post("/audio",
                           data={'id':data["id"],
                                 'uuid':wrong_uuid},
                           files=files)
