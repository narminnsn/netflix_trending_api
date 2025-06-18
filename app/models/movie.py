from sqlalchemy import Column, Integer, String, Date, SmallInteger
from app.core import Base

class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    locale = Column(String(10), nullable=False, index=True)
    release_date = Column(Date, nullable=True)
    runtime = Column(SmallInteger, nullable=True)