from fastapi import APIRouter, Depends, Query, Path, HTTPException
from datetime import date
from sqlalchemy.orm import Session
from typing import Optional
from app.core import get_db
from app.schemas import EngagementResponse
from app.crud import CRUDEngagement

router = APIRouter()
crud_engagement = CRUDEngagement()

@router.get("/v1/title/{id}/engagement",response_model=EngagementResponse)
def get_engagement(
    id: int = Path(..., description="Movie or Season ID"),
    from_date: Optional[date] = Query(None, alias="from"),
    to_date: Optional[date] = Query(None, alias="to"),
    db: Session = Depends(get_db),
):
    result = crud_engagement.get_engagement_timeline(db, id, from_date, to_date)
    if result is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return result