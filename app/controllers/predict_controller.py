from fastapi import APIRouter, Depends, File, HTTPException
from fastapi.datastructures import UploadFile
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

from app.services.jwt_bearer import JWTBearer

router = APIRouter(prefix="/predict")

# Load Model h5 (path ke model)
genre_model = load_model('genre_model.h5')
genre_model.make_predict_function()
genre_labels = { # labels
    0: 'abstract',
    1: 'design',
    2: 'figurative',
    3: 'illustration',
    4: 'landscape',
    5: 'nude painting (nu)',
    6: 'portrait',
    7: 'religious painting',
    8: 'sketch and study',
    9: 'symbolic painting'
}

style_model = load_model('style_model.h5')
style_model.make_predict_function()
style_labels = {
    0: 'Rococo',
    1: 'HighRenaissance',
    2: 'Shin-hanga',
    3: 'NorthernRenaissance', 
    4: 'MagicRealism',
    5: 'Symbolism',
    6: 'Ukiyo-e',
    7: 'Photorealism',
    8: 'FantasticRealism',
    9: 'cartoon',
    10: 'Neo-baroque',
    11: 'Impressionism',
    12: 'FeministArt',
    13: 'Cubo-Futurism',
    14: 'Constructivism',
    15: 'PopArt',
    16: 'Naturalism',
    17: 'NewEuropeanPainting',
    18: 'Divisionism',
    19: 'Academicism',
    20: 'Cubism',
    21: 'Suprematism',
    22: 'Tonalism',
    23: 'ArtNouveau(Modern)',
    24: 'photo',
    25: 'ArtDeco',
    26: 'Realism'
}

era_model = load_model('era_model.h5')
era_model.make_predict_function()
era_labels = {
    0: 'baroque', 
    1: 'contemporary', 
    2: 'impressionism', 
    3: 'medieval', 
    4: 'modern', 
    5: 'neoclassicism', 
    6: 'post impressionism', 
    7: 'primitivism', 
    8: 'realism', 
    9: 'renaissance', 
    10: 'rococo', 
    11: 'romanticism'
}

# preprocess image
def prepare_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Ambil class dengan probability tertinggi dan map index ke corresponding label
def get_highest_probability_class(predictions, class_labels): 
    class_index = np.argmax(predictions)
    class_label = class_labels.get(class_index, 'Unknown')
    return class_index

# endpoint HTTP Post request untuk prediksi
@router.post("/", dependencies=[Depends(JWTBearer())], tags=["predict"])
async def predict(file: UploadFile = File(...)):

    data = {}

    response = {
        "error": True,
        "error_message": "",
        "data" : [data]
    }

    try:
        # save image yg sudah diupload ke folder baru
        image_path = f"uploads/{file.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(file.file.read())

        # preproses imagenya
        processed_image = prepare_image(image_path)

        # Prediksi model genre
        predictions_genre = genre_model.predict(processed_image)
        predicted_genre = get_highest_probability_class(predictions_genre, genre_labels)
        data["genre"] = genre_labels[predicted_genre.item()]

        # Prediksi model style
        predictions_style = style_model.predict(processed_image)
        predicted_style = get_highest_probability_class(predictions_style, style_labels)
        data["style"] = style_labels[predicted_style.item()]

        # Prediksi model era
        predictions_era = era_model.predict(processed_image)
        predicted_era = get_highest_probability_class(predictions_era, era_labels)
        data["era"] = era_labels[predicted_era.item()]

        response["error"] = False

        os.remove(image_path)

    except Exception as e:
        response["error_message"] = e.__context__
        return response

    return response