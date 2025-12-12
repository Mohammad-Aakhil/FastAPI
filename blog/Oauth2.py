from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from . import models, JWTtoken
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ):

    token_data = JWTtoken.verify_access_token(token)

    user_query = await db.execute(select(models.User).where(models.User.id == token_data.user_id))
    user = user_query.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# Reusable RBAC dependency
def require_roles(*allowed_roles: str):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403,
                                detail="Insufficient permissions")
        return current_user
    return role_checker
