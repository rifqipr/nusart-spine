from sqlalchemy import Column, String, text
from app.services.database import Base

from pydantic import BaseModel
from uuid import uuid4

class Art(Base):
    __tablename__ = "arts"

    id          = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()), server_default=text("gen_random_uuid()"))
    image       = Column(String, index=True)
    title       = Column(String, index=True)
    artist      = Column(String, index=True)
    genre       = Column(String, index=True)
    era         = Column(String, index=True)
    description = Column(String, index=True)

class ArtSchema(BaseModel):
    id          : str
    image       : str
    title       : str
    artist      : str
    genre       : str
    era         : str
    description : str
    class Config:
        orm_mode = True