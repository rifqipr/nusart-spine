from typing import List
from fastapi import APIRouter, Depends
from app.models.user import UserCreate
from app.services import crud
from app.services.jwt_handler import signJWT
from app.services.database import get_db
from sqlalchemy.orm import Session

import bcrypt

router = APIRouter(prefix="/users")

# Get all users
@router.get("/", tags=["user"])
async def get_users(skip : int = 0, limit = 100, db : Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    response = {
        "error" : False,
        "error_message" : "",
        "data" : users
    }
    return response

# Get user by id
@router.get("/{id}", tags=["user"])
async def get_user(email : str, db : Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=email)
    if user:
        response = {
            "error" : False,
            "error_message" : "",
            "data" : user
        }
    else:
        response = {
            "error" : True,
            "error_message" : "User does not exist",
            "data" : {}
        }
    return response

# Register
@router.post("/", tags=["user"])
async def create_user(new_user : UserCreate, db : Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, new_user.email)
    if db_user:
        response = {
            "error" : False,
            "error_message" : "Email already registered",
            "data" : {}
        }
    else:
        user = crud.create_user(db, user=new_user)
        response = {
            "error" : False,
            "error_message" : "",
            "data" : user
        }
    return response

# Login
@router.post("/login", tags=["user"])
async def user_login(user : UserCreate, db : Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    response = {
        "error" : True,
        "error_message" : "",
        "data" : {}
    }

    if db_user:
        if bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode('utf-8')):
            return signJWT(user.email)
        response["error_message"] = "Password does not match"
        return response
    else:
        response["error_message"] = "Email not found"
        return response