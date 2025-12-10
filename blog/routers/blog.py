from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, Oauth2
from sqlalchemy.orm import Session
from ..repository import blog
from ..Oauth2 import require_roles, get_current_user

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)


get_db = database.get_db


@router.get("/", response_model=List[schemas.showBlog])
def get_blogs(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def createBlog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(require_roles("user", "editor", "admin"))):
    return blog.create(request, db)


@router.get('/{id}',response_model=schemas.BlogWithUser, status_code=status.HTTP_202_ACCEPTED)
def get_blog(id, db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with item id:{id} is not available")
    return blog


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int, 
                request: schemas.Blog, 
                db: Session = Depends(get_db), 
                # get_current_user: schemas.TokenData = Depends(Oauth2.get_current_user)):
                get_current_user: schemas.TokenData = Depends(require_roles("editor", "admin", "user"))
                ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id:-{id} not found')
    updated = { 
        getattr(models.Blog, key): value
        for key, value in request.model_dump().items()
    }
    blog.update(updated)
    db.commit()
    return {"message": "updated"}


@router.patch('/blogs_patch')
def partial_update(get_current_user: schemas.TokenData = Depends(Oauth2.get_current_user)):
    return "Partial update blog here"


@router.delete('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_blog(id: int, 
                db: Session = Depends(get_db), 
                # get_current_user: schemas.TokenData = Depends(Oauth2.get_current_user)):
                get_current_user = Depends(require_roles("admin"))
                ):
    # blog = db.query(models.Blog).filter(models.Blog.id == id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id:-{id} not found')
    # blog.delete(synchronize_session=False)
    # db.commit()
    # return {'details': f'Blog with id:-{id} deleted successfully'}
    return {'details': "Blog with id:-given deleted successfully"}
