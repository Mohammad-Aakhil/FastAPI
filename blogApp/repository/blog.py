from sqlalchemy.orm import Session
from .. import models, schemas
from sqlalchemy import select, update,delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

# async def get_all(db: AsyncSession):
#     blogs = await db.execute(select(models.Blog))
#     return blogs.scalars().all()

async def get_all(db: AsyncSession, page: int, limit: int):
    offset = (page - 1) * limit

    stmt = (
        select(models.Blog)
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def create(request:schemas.Blog, 
                 db: AsyncSession, 
                 current_user: schemas.TokenData):
    new_blog = models.Blog(title = request.title, 
                           body = request.body, 
                           user_id = current_user.id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


async def show(id :int,
        db: AsyncSession,
        current_user: schemas.TokenData):
    result = await db.execute(select(models.Blog).where(models.Blog.id == id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(404, detail=f"Blog with given id {id} not found")
    return blog

# async def update_SQL(
#         id: int,
#         request: schemas.Blog,
#         db: AsyncSession):
    
#     result = await db.execute(
#         select(models.Blog)
#         .where(models.Blog.id == id ))
#     blog = result.scalar_one_or_none()

#     if not blog:
#         raise HTTPException(404, detail=f"Blog with id:-{id} not found")
#     for key, value in request.model_dump().values():
#         setattr(blog, key, value)
    
#     await db.commit()
#     await db.refresh(blog)

#     return blog



async def update_ORM(
        id: int,
        request: schemas.Blog,
        db: AsyncSession):
    
    await db.execute(
        update(models.Blog)
        .where(models.Blog.id == id)
        .values(**request.model_dump())
    )
    await db.commit()

    result = await db.execute(select(models.Blog).where(models.Blog.id == id))
    return result.scalar_one()     


async def destroy(id: int,
                  db: AsyncSession):
    
    blog_query = await db.execute(select(models.Blog).where(models.Blog.id == id))
    blog = blog_query.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail=f'Blog with id:-{id} not found')
    await db.execute(delete(models.Blog).where(models.Blog.id == id))    
    await db.commit()
    return blog
