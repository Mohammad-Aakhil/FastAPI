from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, database, Oauth2
from ..repository import blog
from ..Oauth2 import require_roles, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import Query

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

from fastapi.security import HTTPBearer
bearer_scheme = HTTPBearer()

get_db = database.get_db


#--------------------------------------------------------------------------------------------------
@router.get("/", response_model=List[schemas.showBlog])
async def get_blogs(db: AsyncSession = Depends(get_db), 
              current_user: schemas.TokenData = Depends(get_current_user),
              page: int | None = Query(1, gt=0),
              limit: int | None = Query(4, gt=0, lt=100)
              ):
    
    # return await blog.get_all(db)
    return await blog.get_all(db, page, limit)


#--------------------------------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogWithUser)
async def createBlog(request: schemas.Blog, 
                     db: AsyncSession = Depends(get_db), 
                     current_user: schemas.TokenData = Depends(require_roles("user", "editor", "admin"))
                     ):
    
    return await blog.create(request, db, current_user)


#--------------------------------------------------------------------------------------------------
@router.get('/{id}',response_model=schemas.BlogWithUser, status_code=status.HTTP_202_ACCEPTED)
async def get_blog(
    id:int, 
    db: AsyncSession = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user)
    ):

    return await blog.show(id, db, current_user)


#--------------------------------------------------------------------------------------------------
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED,
            response_model=schemas.BlogBase)
async def update_blog(id:int, 
                request: schemas.Blog, 
                db: AsyncSession = Depends(get_db), 
                # get_current_user: schemas.TokenData = Depends(Oauth2.get_current_user)):
                current_user: schemas.TokenData = Depends(require_roles("editor", "admin", "user"))
                ):
    
    return await blog.update_ORM(id, request, db)

#--------------------------------------------------------------------------------------------------
@router.patch('/blogs_patch')
async def partial_update(get_current_user: schemas.TokenData = Depends(get_current_user),
                         bearer = Depends(bearer_scheme)):
    
    return "Partial update blog here"

#-------------------------------------------------------------------------------------------------
@router.delete('/blog/{id}',
                status_code=status.HTTP_202_ACCEPTED,
                response_model=schemas.showBlog)

async def delete_blog(id: int, 
                db: AsyncSession = Depends(get_db), 
                current_user = Depends(require_roles("admin"))
                ):
    
    return await blog.destroy(id, db)
