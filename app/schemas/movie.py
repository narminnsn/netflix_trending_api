from pydantic import BaseModel
from datetime import date

class MovieBase(BaseModel):
    title: str
    locale: str
    release_date: date | None = None
    runtime: int | None = None

class MovieInDB(MovieBase):
    id: int

    class Config:
        orm_mode = True