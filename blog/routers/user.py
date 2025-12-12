from fastapi import APIRouter, HTTPException, status, Depends
from .. import database, schemas, models
from ..hashing import Hash
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import users 

router = APIRouter(
    prefix='/user',
    tags=['Users'])

get_db = database.get_db


@router.post('/', response_model=schemas.showUser)
async def create_user(request: schemas.Users, 
                      db: AsyncSession = Depends(get_db)):
    return await users.create(request, db)


@router.get("/", response_model=List[schemas.showUser])
async def get_users(db: AsyncSession = Depends(get_db)):
    
    return await users.get_all_users(db)


@router.get('/{id}', response_model=schemas.showUser)
async def get_user(id:int, 
                   db: AsyncSession= Depends(get_db)):
    
    return await users.get_user(id, db)

