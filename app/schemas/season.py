from pydantic import BaseModel
from datetime import date

class SeasonBase(BaseModel):
    tv_show_id: int
    season_number: int
    release_date: date | None = None
    runtime: int | None = None

class SeasonInDB(SeasonBase):
    id: int

    class Config:
        orm_mode = True
