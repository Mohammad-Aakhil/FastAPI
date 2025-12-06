from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title : str
    body: str
    # class Config():
    #     from_attributes = True

class Blog(BlogBase):
    class Config():
        from_attributes = True


class Users(BaseModel):
    name : str
    email: str  
    password: str 


class showUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    class Config():
        from_attributes = True


class showBlog(Blog):
    title : str
    body: str
    creator: showUser
    class Config():
        # orm_mode = True
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name:str| None = None
    email: str | None = None

