from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED
from .utils import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import User
from .config import setting



oauth2 = OAuth2PasswordBearer(tokenUrl='login')

from app import schema



def create_token(data: dict):

    plain = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=setting.access_token_expire_minutes)
    plain.update({"exp": expire.timestamp()})
    cipher = jwt.encode(plain, setting.secret_key, algorithm=setting.algorithm)
    return cipher

def verify_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        payload_id : str = payload.get("user_id")

        if not payload_id:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='No token exists with this id')

        token_data = schema.TokenData(id=payload_id)
        return token_data
    except PyJWTError:
        raise credential_exception


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Invalid credential detail')

    t =  verify_token(token, credential_exception)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Invalid token')

    
    
    stmt = select(User).where(User.id == t.id)
    u = db.execute(stmt).scalar_one()

    if not u:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Not authorized to access the resource')

    return u
    

