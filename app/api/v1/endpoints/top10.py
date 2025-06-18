from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Literal
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.schemas import Top10Item
from app.core import get_db
from app.crud import CRUDTop10

router = APIRouter()
crud_top10 = CRUDTop10()

@router.get("/v1/top10", response_model=List[Top10Item])
def get_top10(
    locale: str = Query(..., description="Language/market of interest"),
    window: Literal["WEEKLY", "SEMI_ANNUALLY"] = Query("WEEKLY"),
    as_of: date | None = Query(None),
    include: Literal["movie", "season", "both"] = Query("both"),
    db: Session = Depends(get_db),
):
    results = crud_top10.get_top10(db, locale, window, as_of, include)
    if not results:
        raise HTTPException(status_code=404, detail="No data found for the given parameters.")
    return results