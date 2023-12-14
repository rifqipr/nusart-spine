from sqlalchemy.orm import Session
from app.models.user import UserCreate, User
from app.models.art import Art

import bcrypt

# user table
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(email=user.email, password=hashed_password.decode("utf-8"))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# art table
def get_arts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Art).offset(skip).limit(limit).all()

def get_art(db: Session, art_id: str):
    return db.query(Art).filter(Art.id == art_id).first()

def get_art_by_title(db: Session, title: str):
    return db.query(Art).filter(Art.title == title).first()

def create_art(db: Session, art: Art):
    db_art = Art(image=art.image, title=art.title, artist=art.artist, genre=art.genre, era=art.era, description=art.description)
    db.add(db_art)
    db.commit()
    db.refresh(db_art)
    return db_art