from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


#for sending back response
class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime 
    owner_id: int
    owner : UserOut

    class Config:  # this is required because pydantic by default only works with dictionaries but SQLAlchemy models are not dictionaries, so we need to tell pydantic to work with SQLAlchemy models also
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    vote_dir: int  # 1 means like, 0 means unlike
