from pydantic import BaseModel

class Top10Item(BaseModel):
    id: int
    type: str
    title: str
    view_rank: int
    hours_viewed: int
    views: int
    runtime: int