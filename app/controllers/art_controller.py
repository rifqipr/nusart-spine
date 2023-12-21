from fastapi import APIRouter, Depends, File
from fastapi.datastructures import UploadFile
from app.models.art import CreateArt
from app.services import crud, gcs
from app.services.jwt_bearer import JWTBearer
from app.services.database import get_db
from sqlalchemy.orm import Session

import os

router = APIRouter(prefix="/arts")

# Get all arts
@router.get("/", dependencies=[Depends(JWTBearer())], tags=["art"])
async def get_arts(skip : int = 0, limit = 100, db : Session = Depends(get_db)):
    arts = crud.get_arts(db, skip=skip, limit=limit)
    response = {
        "error" : False,
        "error_message" : "",
        "data" : arts
    }
    return response

# Get art by ID
@router.get("/{art_id}", dependencies=[Depends(JWTBearer())], tags=["art"])
async def get_art(id : str, db : Session = Depends(get_db)):
    db_art = crud.get_art(db, id)
    if db_art:
        response = {
            "error" : False,
            "error_message" : "",
            "data" : [db_art]
        }
    else:
        response = {
            "error" : True,
            "error_message" : "Art not found",
            "data" : []
        }
    return response

# Post Art to DB
@router.post("/gallery", dependencies=[Depends(JWTBearer())], tags=["art"])
async def upload_art(data : CreateArt, db : Session = Depends(get_db)):
    new_art = crud.create_art(db, data)
    response = {
        "error" : False,
        "error_message" : "",
        "data" : [new_art]
    }
    return response

# Post Art (Predict)
# @router.post("/pred", dependencies=[Depends(JWTBearer())], tags=["art"])
# async def upload_art_pred(file : UploadFile = File(...)):
#     allowed_extensions = {'jpg', 'jpeg', 'png'}
#     file_extension = os.path.splitext(file.filename)[1].lower()[1:]
#     if file_extension not in allowed_extensions:
#         response = {
#             "error" : False,
#             "error_message" : "Invalid Document Type",
#             "data" : []
#         }
    
#     else:
#         new_img = gcs.upload_pred(file)
#         response = {
#             "error" : False,
#             "error_message" : "",
#             "data" : [new_img]
#         }
#     return response