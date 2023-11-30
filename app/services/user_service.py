from passlib.hash import bcrypt
from firebase_admin import firestore
from app.models.user import User, UserCreate

class UserService:
    @staticmethod
    def create_user(user: UserCreate):
        db = firestore.client()
        user_data = user.dict()
        # Hash the password before storing it
        user_data["password"] = bcrypt.hash(user.password)
        user_data["role"] = "User"  # Default role
        db.collection("users").document(user.email).set(user_data)

    @staticmethod
    def get_user(email: str):
        db = firestore.client()
        user_data = db.collection("users").document(email).get()
        if user_data.exists:
            return User(**user_data.to_dict())

    @staticmethod
    def authenticate_user(email: str, password: str):
        db = firestore.client()
        user_data = db.collection("users").document(email).get()
        if user_data.exists:
            stored_password = user_data.to_dict().get("password", "")
            # Verify the hashed password
            return bcrypt.verify(password, stored_password)
        return False