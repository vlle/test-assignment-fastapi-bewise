from pydantic import BaseModel
from pydantic.types import UUID4


class UserInput(BaseModel):
    nick: str

    class Config:
        schema_extra = {
            "example": {
                "nick": "vlle",
            }
        }


class UserOutput(BaseModel):
    id: int
    uuid: UUID4

    class Config:
        schema_extra = {
            "example": {
                "id": "42",
                "uuid": "123e4567-e89b-12d3-a456-426655440000",
            }
        }
