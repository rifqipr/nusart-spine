from fastapi import FastAPI
from app.controllers import art_controller, user_controller
from app.services.database import init_db

app = FastAPI()

app.include_router(art_controller.router)
app.include_router(user_controller.router)

if __name__ == "__main__":
    init_db()