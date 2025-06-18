from sqlalchemy import Column, Integer, ForeignKey, Date, SmallInteger
from sqlalchemy.orm import relationship
from app.core import Base

class Season(Base):
    __tablename__ = "season"

    id = Column(Integer, primary_key=True, index=True)
    tv_show_id = Column(Integer, ForeignKey("tv_show.id"), nullable=False, index=True)
    season_number = Column(SmallInteger, nullable=False)
    release_date = Column(Date, nullable=True)
    runtime = Column(SmallInteger, nullable=True)

    tv_show = relationship("TVShow", backref="seasons")
