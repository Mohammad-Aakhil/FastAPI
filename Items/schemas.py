from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int


class CreateBook(BookBase):
    pass


class Book(BookBase):
    id: int

    class confiq:
        # orm_mode = True   ##for pydantic version < 2.x
        from_attributes  : True  #for pydantic version > 2.x
