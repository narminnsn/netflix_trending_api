from sqlalchemy import Column, Integer, String
from app.core import Base

class TVShow(Base):
    __tablename__ = "tv_show"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    locale = Column(String(10), nullable=False, index=True)