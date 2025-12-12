from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import User
from .. import models, hashing
from fastapi import HTTPException 

async def create(request, db: AsyncSession):

    new_user = models.User(
        name=request.name, 
        email=request.email, 
        password=hashing.Hash.argon2(request.password), role=request.role )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_all_users(db: AsyncSession):
    query = await db.execute(select(User))
    users = query.scalars().all()
    return users

async def get_user(id, db):
    query = await db.execute(
        select(models.User).where(models.User.id == id))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(404, detail=f'User with id:-{id} not found')
    
    return user
