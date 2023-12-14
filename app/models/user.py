from sqlalchemy import Column, String, text
from typing import Optional
from app.services.database import Base

from pydantic import BaseModel, EmailStr
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id              = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()), server_default=text("gen_random_uuid()"))
    email           = Column(String, index=True)
    fullname        = Column(String, nullable=True, index=True)
    phone           = Column(String, nullable=True, index=True)
    domicile        = Column(String, nullable=True, index=True)
    password        = Column(String, index=True)

class UserBase(BaseModel):
    email       : EmailStr

class UserCreate(UserBase):
    password   : str

class UserSchema(UserBase):
    id          : str
    fullname    : Optional[str] = None
    phone       : Optional[str] = None
    domicile    : Optional[str] = None

    class Config:
        orm_mode = True