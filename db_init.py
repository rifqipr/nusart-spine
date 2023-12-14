from app.models import Base
from app.services.database import engine

def init_db():
    Base.metadata.create_all(bind=engine)

def main():
    init_db()

if __name__ == "__main__":
    main()
