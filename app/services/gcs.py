from google.cloud import storage
from fastapi import UploadFile
from google.auth import default

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "capstone-nusart-901e701ec3c9.json"
credentials, project = default()

storage_client = storage.Client.from_service_account_json("capstone-nusart-901e701ec3c9.json")
gallery_bucket = storage_client.get_bucket('nusart-gallery')
prediction_bucket = storage_client.get_bucket('nusart-pred')

def upload_gallery(file : UploadFile):
    blob = prediction_bucket.blob(file.filename)
    blob.upload_from_file(file.file)

    url = f"https://storage.googleapis.com/nusart-gallery/{file.filename}"
    return url

def upload_pred(file : UploadFile):
    blob = prediction_bucket.blob(file.filename)
    blob.upload_from_file(file.file)

    url = f"https://storage.googleapis.com/nusart-pred/{file.filename}"
    return {"image_url" : url}