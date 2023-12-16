from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserSchema,  UserCreate
from app.services import crud
from app.services.jwt_handler import signJWT
from app.services.database import get_db
from sqlalchemy.orm import Session

import bcrypt

router = APIRouter()

# Get all users
@router.get("/users", response_model=List[UserSchema], tags=["user"])
async def get_users(skip : int = 0, limit = 100, db : Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Get user by id
@router.get("/users/{id}", response_model=List[UserSchema], tags=["user"])
async def get_user(email : str, db : Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=email)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User does not exist")

# Register
@router.post("/users", tags=["user"])
async def create_user(newUser : UserCreate, db : Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, newUser.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user=newUser)

# Login
@router.post("/users/login", tags=["user"])
async def user_login(user : UserCreate, db : Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if db_user:
        if bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode('utf-8')):
            return signJWT(user.email)
        raise HTTPException(status_code=401, detail="Password does not match")
    else:
        raise HTTPException(status_code=401, detail="Email does not exist")