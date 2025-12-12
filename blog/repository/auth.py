from sqlalchemy import select
from .. import models, hashing, JWTtoken
from fastapi import HTTPException
from ..JWTtoken import create_access_token, create_refresh_token, verify_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession

async def login_db(request, db: AsyncSession):
    user_query = await db.execute(
        select(models.User).where(models.User.name == request.username))
    user = user_query.scalar_one_or_none()

    if not user or not hashing.Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id, "role": user.role})
    refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_db(refresh_token: str):
    user_id, role = verify_refresh_token(refresh_token)
    new_access_token = create_access_token({"user_id": user_id, "role": role})
    return {"access_token": new_access_token, "token_type": "bearer"}
