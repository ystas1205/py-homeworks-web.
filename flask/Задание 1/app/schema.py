from typing import Optional
import pydantic
from abc import ABC


class AbstractUser(pydantic.BaseModel, ABC):
    title: str
    description: str
    user: str


class CreateUser(AbstractUser):
    title: str
    description: str
    user: str


class UpdateUser(AbstractUser):
    title: Optional[str] = None
    description: Optional[str] = None
    user: Optional[str] = None
