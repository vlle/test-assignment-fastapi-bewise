from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Audio, User

from app.schemas import UserInput, UserOutput


async def save_user(session: AsyncSession, user: UserInput) -> UserOutput:
    async with session.begin():
        u = User(name=user.nick)
        session.add(u)
    return UserOutput(id=u.id, uuid=u.uuid)


async def is_there_user(session: AsyncSession, user: UserOutput) -> bool:
    stmt = select(User).where(and_(User.id == user.id, User.uuid == user.uuid))
    async with session.begin():
        u = (await session.scalars(stmt)).one_or_none()
    return u is not None


async def save_music(session: AsyncSession, file: str, user_id: int) -> int:
    async with session.begin():
        u = Audio(filepath=file, user_id=user_id)
        session.add(u)
    return u.id


async def is_user_uploaded_audio(
    session: AsyncSession, audio_id: int, user_id: int
) -> bool:
    stmt = (
        select(Audio).join(User).where(and_(Audio.id == audio_id, User.id == user_id))
    )
    async with session.begin():
        u = (await session.scalars(stmt)).one_or_none()
    return u is not None


async def select_audio(session: AsyncSession, audio_id) -> Audio | None:
    stmt = select(Audio).where(Audio.id == audio_id)
    async with session.begin():
        u = (await session.scalars(stmt)).one_or_none()
    return u
