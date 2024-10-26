"""Module defines utils pydantic schemas for app"""

from pydantic import BaseModel


class CreateResultSchema(BaseModel):
    id: int
