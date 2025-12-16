from fastapi import APIRouter, Depends
from .. import database
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import auth

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db


@router.post("/login", status_code=202)
async def login(request: OAuth2PasswordRequestForm = Depends(), 
                db: AsyncSession  = Depends(get_db)
                ):

    return await auth.login_db(request, db)

@router.post("/refresh")
async def refresh_token(refresh_token: str):

    return await auth.refresh_db(refresh_token)

