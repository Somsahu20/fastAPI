from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from typing import Optional, List
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
import psycopg2, time
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from .. import models, schema
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_201_CREATED

from ..database import engine
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from .. import utils
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hashing(password):
    return password_hash.hash(password)



my_posts = [{"name": "Naman", "surname": "Tyagi", "is_married": True}, {"mame": "Rezz", "surname": "Yadav", "is_married": True}];





@router.post('/user/create', status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(u: schema.User, db: Session = Depends(utils.get_db)):

    try:
        
        user = u.model_dump()
        hashed_pass = hashing(user["password"])
        user["password"] = hashed_pass
        new_user = models.User(**user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as err:
        print("Error at creating error")
        db.rollback()
        print("Error is", err)
        raise HTTPException(status_code='404', detail='Can\'t add new user')


@router.get('/user/{id}', response_model=schema.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(utils.get_db)):

    try:
        stmt = select(models.User).where(models.User.id == id)
        u = db.execute(stmt).scalar_one()

        return u
    except Exception as err:
        print("Error at get user by id")
        print("Error is ", err)
        raise HTTPException(status_code=404, detail='User not found')


@router.delete('/deleteuser/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(utils.get_db)):

    try:
        stmt = select(models.User).where(models.User.id == id)
        u = db.execute(stmt).scalar_one()

        if not u:
            raise HTTPException(status_code=404, detail='No user with such id')

        db.delete(u)
        db.commit()
        return None

    except Exception as err:
        print("Error in deleting user")
        print('Error is', err)
        db.rollback()
        raise HTTPException(status_code=404, detail='Can\'t delete user')