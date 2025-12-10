from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from .database import Base
from sqlalchemy.orm import relationship
import enum

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User", back_populates="blogs")


class Roles(str, enum.Enum):
    user = "user"
    editor = "editor"
    admin = "admin"


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(Roles), default=Roles.user, nullable=False)
    blogs = relationship('Blog', back_populates="creator")



