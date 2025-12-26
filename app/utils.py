from .database import *

def get_db():
    db = sessionLocal() 
    try:
        yield db
    finally:
        db.close()