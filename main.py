from fastapi import FastAPI 
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    description: Optional[bool]


@app.get("/")
def showBlogs():
    return {"data": 'FastAPI get method'}

def index():
    pass


@app.post('/blog')
def create_blog(request: Blog):
    return f"Blog isn created with title {request.title}"

