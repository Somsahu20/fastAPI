from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class Post(BaseModel):
    name: str
    surname: str
    is_married: bool = False

class CreatePost(Post):
    pass



class User(BaseModel):
    email: EmailStr
    password: str

    # model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class Vote(BaseModel):
    post_id: int
    direction: int = Field(ge=0, le=0)


class VoteGive(BaseModel):
    post_id: int
    direction: int = Field(ge=0, le=1)

class PostResponse(BaseModel):
    name: str
    surname: str
    is_married: bool = False
    # user_id: int
    user: UserResponse

    model_config = ConfigDict(from_attributes=True) #! Needed to configure the pydantic model to configure automatically top response model

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

class VoteResponse(BaseModel):
    post: PostResponse

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
