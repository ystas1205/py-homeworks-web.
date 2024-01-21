from typing import Optional
import pydantic
from abc import ABC


class AbstractUser(pydantic.BaseModel, ABC):
    title: str
    description: str
    user: str



    # @pydantic.field_validator("password")
    # @classmethod
    # def secure_password(cls, v: str) -> str:
    #     if len(v) < 8:
    #         raise ValueError(f"Minimal length of password is 8")
    #     return v


class CreateUser(AbstractUser):
    title: str
    description: str
    user: str



class UpdateUser(AbstractUser):
    title: Optional[str] = None
    description: Optional[str] = None
    user: Optional[str] = None

