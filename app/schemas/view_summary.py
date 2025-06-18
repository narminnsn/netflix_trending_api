from pydantic import BaseModel
from datetime import date

class ViewSummaryBase(BaseModel):
    duration: str
    start_date: date
    end_date: date | None = None
    view_rank: int
    hours_viewed: int
    views: int
    movie_id: int | None = None
    season_id: int | None = None

class ViewSummaryInDB(ViewSummaryBase):
    id: int

    class Config:
        orm_mode = True
