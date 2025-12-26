from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from ..utils import get_db
from ..models import User, Posts
from ..schema import UserLogin, UserResponse, Token
from .users import password_hash
from ..oauth import create_token

router = APIRouter(tags=['authentication'])

@router.post('/login', response_model=Token)
def login(u: UserLogin, db: Session = Depends(get_db)):

    try:
        stmt = select(User).where(User.email == u.email)
        req_user = db.execute(stmt).scalar_one()
        
        stored_password = req_user.password
        # recieved_password = hashing(u.password)
        received_password = u.password

        if not password_hash.verify(received_password, stored_password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Wrong Password, try again')
        
        # return {"message": "Successfully created the token"}
        token = create_token(data={"user_id": req_user.id})
        return {"access_token": token, "token_type": "bearer"}
        # return token
        

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
   
    except Exception as err:
        print('Error in login')
        print('Error is ', err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in login')

