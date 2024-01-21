from typing import Optional
import pydantic


class CreateToken(pydantic.BaseModel):
    user: str
    email: str
    password: str

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f"Minimal length of password is 8")
        return v


class CreateAnnouncement(pydantic.BaseModel):
    title: str
    description: str
    user_id: int


class UpdateAnnouncement(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
