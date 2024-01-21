from .db.database import get_db_connection

def get_database():
    try:
        db = get_db_connection()
        yield db
    finally:
        db.close()
