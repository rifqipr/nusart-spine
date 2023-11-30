from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
# from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from app.controllers.user_controller import UserController, User, UserCreate

# load_dotenv()

# Firebase initialization
cred = credentials.Certificate("app/google-services.json")
initialize_app(cred)

app = FastAPI()

# Routes
@app.post("/register", response_model=None)
async def register(user: UserCreate):
    UserController.register_user(user)

@app.post("/login", response_model=dict)
async def login(user: User):
    return UserController.login_user(user.email, user.password)

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(UserController.get_current_user)):
    return current_user