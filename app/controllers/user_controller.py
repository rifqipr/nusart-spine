from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from pydantic import BaseModel
from typing import List
from app.services.user_service import UserService
from app.models.user import User, UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserController:
    @staticmethod
    def register_user(user: UserCreate):
        UserService.create_user(user)

    @staticmethod
    def login_user(email: str, password: str):
        if UserService.authenticate_user(email, password):
            return {"token_type": "bearer", "access_token": email}

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        return UserService.get_user(token)
