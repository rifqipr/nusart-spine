from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.models.art import Art, ArtSchema
from app.services import crud
from app.services.jwt_bearer import JWTBearer
from app.services.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Get all arts
@router.get("/arts", dependencies=[Depends(JWTBearer())], response_model=List[ArtSchema], tags=["art"])
def get_arts(skip : int = 0, limit = 100, db : Session = Depends(get_db)):
    arts = crud.get_arts(db, skip=skip, limit=limit)
    return arts

# Get art by ID
@router.get("/arts/{art_id}", dependencies=[Depends(JWTBearer())], response_model=ArtSchema, tags=["art"])
def get_art(id : str, db : Session = Depends(get_db)):
    db_art = crud.get_art(db, id)
    if db_art in None:
        raise HTTPException(status_code=404, detail="Art not found")
    return db_art

# Post Art
@router.post("/arts", response_model=ArtSchema, tags=["art"])
async def upload_art(art : ArtSchema, db : Session = Depends(get_db)):
    return crud.create_art(db, art=art)