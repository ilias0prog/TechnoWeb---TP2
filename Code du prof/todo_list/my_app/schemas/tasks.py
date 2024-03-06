from datetime import date

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    name: str = Field(min_length=3, max_length=50)
    description: str
    creation_date: date
