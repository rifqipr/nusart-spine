from fastapi import FastAPI, Body, Depends
from app.models.user import User, UserLogin
from app.services.jwt_handler import signJWT
from app.services.jwt_bearer import JWTBearer

arts = [
    {
        "id" : 1,
        "image_url" : "example_url",
        "title" : "demo",
        "artist" : "Pradipta",
        "genre" : "Post-Romantic",
        "era" : "Classical (1667)",
        "description" : "Lorem ipsum dolor sit amet"
    },
    {
        "id" : 2,
        "image_url" : "example_url2",
        "title" : "demo2",
        "artist" : "Pradipta2",
        "genre" : "Post-Romantic2",
        "era" : "Classical (1667)2",
        "description" : "Lorem ipsum dolor sit amet2"
    },
    {
        "id" : 3,
        "image_url" : "example_url3",
        "title" : "demo3",
        "artist" : "Pradipta3",
        "genre" : "Post-Romantic3",
        "era" : "Classical (1667)3",
        "description" : "Lorem ipsum dolor sit amet3"
    }
]

users = []

app = FastAPI()

@app.get("/", tags=["test"])
def greet():
    return {"Hello" : "World"}

@app.get("/arts", dependencies=[Depends(JWTBearer())], tags=["art"])
def get_arts():
    return {"data" : arts}

@app.get("/art/{id}", dependencies=[Depends(JWTBearer())], tags=["art"])
def get_one_arts(id : int):
    if id > len(arts):
        return {
            "error" : "Post with this ID does not exist"
        }
    for art in arts:
        if art["id"] == id:
            return {
                "data" : art
            }
        
@app.get("/users", tags=["user"])
def get_userss():
    return {"data" : users}

@app.post("/user/signup", tags=["user"])
def user_signup(user : User = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data : UserLogin):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False
    
@app.post("/user/login", tags=["user"])
def user_login(user : UserLogin = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error" : "Invalid Login"
        }