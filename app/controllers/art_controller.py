from typing import List
from fastapi import APIRouter, Depends, HTTPException, File
from fastapi.datastructures import UploadFile
from app.models.art import ArtSchema, CreateArt
from app.services import crud, gcs
from app.services.jwt_bearer import JWTBearer
from app.services.database import get_db
from sqlalchemy.orm import Session

import os

router = APIRouter()

# Get all arts
@router.get("/arts", dependencies=[Depends(JWTBearer())], response_model=List[ArtSchema], tags=["art"])
async def get_arts(skip : int = 0, limit = 100, db : Session = Depends(get_db)):
    arts = crud.get_arts(db, skip=skip, limit=limit)
    return arts

# Get art by ID
@router.get("/arts/{art_id}", dependencies=[Depends(JWTBearer())], response_model=ArtSchema, tags=["art"])
async def get_art(id : str, db : Session = Depends(get_db)):
    db_art = crud.get_art(db, id)
    if db_art in None:
        raise HTTPException(status_code=404, detail="Art not found")
    return db_art

# Post Art to DB
@router.post("/arts/gallery", dependencies=[Depends(JWTBearer())], response_model=ArtSchema, tags=["art"])
async def upload_art(data : CreateArt, db : Session = Depends(get_db)):
    return crud.create_art(db, data)

# Post Art (Predict)
@router.post("/arts/pred", dependencies=[Depends(JWTBearer())], tags=["art"])
async def upload_art_pred(file : UploadFile = File(...)):
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    file_extension = os.path.splitext(file.filename)[1].lower()[1:]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid document type")
    
    return gcs.upload_pred(file)