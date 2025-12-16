from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    title : str
    body: str


class Blog(BlogBase):
    class ConfigDict():
        from_attributes = True


class Users(BaseModel):
    name : str
    email: str  
    password: str
    role: str 


class showUser(BaseModel):
    name: str
    email: str
    role: str
    # blogs: List[Blog] = []
    class ConfigDict():
        from_attributes = True


class showBlog(Blog):
    id: int
    title : str
    body: str
    creator: showUser
    class ConfigDict():
        # orm_mode = True
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    role: str
    type: str

##----------------------------------------------------
class UserBase(BaseModel):
    id: int
    name: str
    email: str

    class ConfigDict:
        from_attributes = True

class BlogWithUser(BlogBase):
    creator: UserBase
    