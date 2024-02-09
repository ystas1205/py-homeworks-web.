from typing import Optional
import pydantic
import json
from aiohttp import web


def get_http_error(error_class, message):
    return error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )


class CreateToken(pydantic.BaseModel):
    user: str
    email: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise get_http_error(web.HTTPBadRequest,
                                 f"Minimal length of password is 8")
        return v


class CreateAnnouncement(pydantic.BaseModel):
    title: str
    description: str
    user_id: int


class UpdateAnnouncement(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
