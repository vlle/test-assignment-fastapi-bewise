from pydantic import UUID4
from sqlalchemy import UUID, ForeignKey, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID4] = mapped_column(UUID, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"""
                User(id={self.id},
                    name={self.name})
                    uuid={self.uuid})
                """


class Audio(Base):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    mp3: Mapped[str] = mapped_column(String(100))
    uuid: Mapped[UUID4] = mapped_column(UUID, server_default=text("gen_random_uuid()"))

    def __repr__(self) -> str:
        return f"""
                Audio(id={self.id},
                    name={self.mp3})
                    uuid={self.uuid})
                """
