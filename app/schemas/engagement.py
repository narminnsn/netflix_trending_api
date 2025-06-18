from pydantic import BaseModel
from typing import List, Optional

class TimelineItem(BaseModel):
    start_date: str
    hours_viewed: int
    views: int
    view_rank: Optional[int]

class EngagementResponse(BaseModel):
    id: int
    type: str
    title: str
    timeline: List[TimelineItem]