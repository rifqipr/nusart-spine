from fastapi.responses import JSONResponse
from jose import jwt
from decouple import config
import time

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")

def token_response(token : str):
    response = {
        "error" : False,
        "error_message" : "",
        "data" : {
            "access_token" : token
            }
    }
    return JSONResponse(content=response, status_code=200)

def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 2
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}