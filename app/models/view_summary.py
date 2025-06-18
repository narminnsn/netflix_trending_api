from sqlalchemy import Column, Integer, String, Date, SmallInteger, BigInteger, ForeignKey
from app.core import Base

class ViewSummary(Base):
    __tablename__ = "view_summary"

    id = Column(Integer, primary_key=True, index=True)
    duration = Column(String(20), nullable=False)  # WEEKLY / SEMI_ANNUALLY
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=True)
    view_rank = Column(SmallInteger, nullable=False, index=True)
    hours_viewed = Column(BigInteger, nullable=False)
    views = Column(BigInteger, nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=True, index=True)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=True, index=True)