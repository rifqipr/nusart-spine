from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self, auto_Error : bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request : Request):
        credentials : HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 401, details="Token Invalid or Expired")
            return credentials.credentials
        else:
            raise HTTPException(status_code = 401, details="Token Invalid or Expired")
    
    def verify_jwt(self, jtwtoken : str):
        isTokenValid : bool = False
        payload = decodeJWT(jtwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid