from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel,Field
from uuid import UUID, uuid4

app = FastAPI()

# @app.get('/')
# def message():
#     return 'this is an fast api end point'



# @app.get('/about')
# def about():
#     return 'This is an about page'



# @app.get('/blog/unpublished')
# def unpublished():
#     return 'All Unpublished Blogs'

# @app.get('/blogs/{id}')
# def singleBlogs(id):
#     return f'Your requested blog, {id}'



# @app.get('/blogs/{id}/comments')
# def singleBlogsComment(id:int):
#     return f'Your requested blog comment is, {id}'



# @app.get('/blog/')
# def index(limit = 10, published: bool =True, sort:Optional[str] = None):
#     if published:
#         return f"{limit} published blog from bd"
#     else:
#         return f"{limit} blog from bd"


class Book(BaseModel):
    id : UUID
    title: str = Field(min_length=1)
    author: str =  Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating :int = Field(gt=1, lt=100)


Books = []

@app.get('/')
def allBooks():
    return Books


@app.post('/addBook/')
def addBook(book:Book):
    Books.append(book)
    return {"data": book}

@app.put('/{book_id}')
def updateBook(book_id: UUID, book: Book):
    counter = 0

    for each in Books:
        counter +=1
        if each.id == book_id:
            Books[counter-1] = book
            return Books[counter-1]
    
    raise HTTPException(
        status_code=404,
        detail= f'ID {book_id} Does not exist'
    )


@app.delete('/{deleteBook}')
def removeBook(book_id: UUID):
    counter = 0

    for each in Books:
        counter+=1
        if each.id == book_id:
            del Books[counter-1]
            return f"ID {book_id} was deleted"

    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} Does not exist"
    )      


    