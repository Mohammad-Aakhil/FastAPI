from fastapi import APIRouter, HTTPException, status, Depends
from .. import database, schemas, models
from ..hashing import Hash
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import users 
from ..Oauth2 import require_roles, get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Users'])

get_db = database.get_db


@router.post('/', response_model=schemas.showUser)
async def create_user(request: schemas.Users, 
                      db: AsyncSession = Depends(get_db)):
    
    return await users.create(request, db)


@router.get("/", response_model=List[schemas.showUser])
async def get_users(db: AsyncSession = Depends(get_db), 
                    curr_user : schemas.TokenData =Depends(require_roles("admin"))):
    
    return await users.get_all_users(db, curr_user)


@router.get("/rbac", response_model=List[schemas.showUser] | schemas.showUser)
async def get_users_by_role(db: AsyncSession = Depends(get_db),
                            curr_user: schemas.TokenData = Depends(get_current_user)):
    
    return await users.get_roleBased_users(db, curr_user)


@router.get('/{id}', response_model=schemas.showUser)
async def get_user(id:int, 
                   db: AsyncSession= Depends(get_db)):
    
    return await users.get_user(id, db)

