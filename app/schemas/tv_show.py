from pydantic import BaseModel

class TVShowBase(BaseModel):
    title: str
    locale: str

class TVShowInDB(TVShowBase):
    id: int

    class Config:
        orm_mode = True