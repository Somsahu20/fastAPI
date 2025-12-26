
from fastapi import FastAPI
from fastapi import Body, Depends
from fastapi.exceptions import ResponseValidationError
from pydantic import BaseModel
from typing import Optional, List
import psycopg2, time
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from . import models, schema
from .database import *
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from .routers import posts, users, authentication, vote
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# li = [
#     "https://www.google.com",
#     "https://www.youtube.com"
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Hello World"}

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)
app.include_router(vote.router)










