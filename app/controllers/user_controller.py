from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserSchema,  UserCreate
from app.services import crud
from app.services.jwt_handler import signJWT
from app.services.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Get all users
@router.get("/users", response_model=List[UserSchema], tags=["user"])
async def get_users(skip : int = 0, limit = 100, db : Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=List[UserSchema], tags=["user"])
async def get_users(email : str, db : Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=email)
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"Email {email} is not registered")

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

    if db_user and user.password == db_user.password:
        return signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail="Invalid Login")