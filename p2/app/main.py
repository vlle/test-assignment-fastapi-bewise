from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, Form, HTTPException, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from pydantic import UUID4
from pydub.audio_segment import CouldntDecodeError
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import init_models, maker, engine
from app.schemas import UserInput, UserOutput
from app.crud import (
    is_there_user,
    save_music,
    save_user,
    is_user_uploaded_audio,
    select_audio,
)
from pydub import AudioSegment
from io import BytesIO


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


@app.post("/user", status_code=201)
async def create_user(user: UserInput, session: AsyncSession = Depends(db_connection)):
    try:
        return await save_user(session, user)
    except DataError:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="wrong data size"
        )


@app.post("/audio", status_code=201)
async def save_as_mp3_and_convert_link(
    id: Annotated[str, Form()],
    uuid: Annotated[UUID4, Form()],
    file: UploadFile,
    request: Request,
    session: AsyncSession = Depends(db_connection),
):
    user = UserOutput(id=int(id), uuid=uuid)
    is_user_registered = await is_there_user(session, user)
    if not is_user_registered:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="user was not found")

    music_buff = BytesIO()
    wav_file = await file.read()
    try:
        sound = AudioSegment.from_wav(BytesIO(wav_file))

        sound.export(music_buff, format="mp3")
        music_buff.seek(0)
    except CouldntDecodeError:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="wrong format, use .wav"
        )
    try:
        audio_id = await save_music(session, music_buff, user.id)
        download_link = (
            str(request.url_for("get_audio")) + "?id={audio_id}&user={user_id}"
        )
        link = download_link.format(audio_id=audio_id, user_id=user.id)
        return {"link": link}
    except IntegrityError:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, detail="integrity error in database"
        )


@app.get("/record")
async def get_audio(id: int, user: int, session: AsyncSession = Depends(db_connection)):
    audio = await select_audio(session, id)
    if not audio:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="no such file")
    is_user_allowed_to_download = await is_user_uploaded_audio(session, id, user)
    if not is_user_allowed_to_download:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="you are not allowed to download file"
        )
    return StreamingResponse(BytesIO(audio.mp3), media_type="audio/mpeg")
