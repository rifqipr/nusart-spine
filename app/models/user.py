from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email           : EmailStr
    fullname        : str | None = None
    phone           : str | None = None
    domicile        : str | None = None
    password        : str
    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "fullname": "Joe Doe",
                "phone": "081387879090",
                "domicile": "Jakarta",
                "password": "any",
            }
        }

class UserLogin(BaseModel):
    email       : EmailStr
    password    : str
    class Config:
        schema_extra = {
            "example": {
                "email" : "joe@xyz.com",
                "password": "any"
            }
        }