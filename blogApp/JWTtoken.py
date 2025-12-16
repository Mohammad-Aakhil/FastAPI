from datetime import datetime, timedelta, timezone
from . import schemas
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
from blogApp.core.config import settings

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
REFRESH_SECRET_KEY  = "c77fd74ebcda6fa4d1006584d90a3e75292407a185505749937853463fa57dc4"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_EXPIRE = 60 * 24 * 7


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "access"
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        role = payload.get("role")
        token_type = payload.get("type")

        if token_type != "access":
            raise InvalidTokenError("Invalid token type")

        if user_id is None or role is None:
            raise InvalidTokenError("Invalid token payload")

        return schemas.TokenData(user_id=user_id, role=role, type=token_type)

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or malformed token")


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        role = payload.get("role")
        token_type = payload.get("type")

        if token_type != "refresh":
            raise InvalidTokenError("Invalid token type")

        if user_id is None or role is None:
            raise InvalidTokenError("Invalid token payload")

        return schemas.TokenData(user_id=user_id, role=role, type=token_type)

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or malformed token")

