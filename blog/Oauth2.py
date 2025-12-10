from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from . import models, JWTtoken
from .database import get_db
from fastapi.security import OAuth2PasswordBearer

from . import JWTtoken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# def get_current_user(token: str = Depends(oauth2_scheme),  
#     db: Session = Depends(get_db)) -> models.User:

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},     
#     )
#     return JWTtoken.verify_token(token, credentials_exception)


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ):

    try:
        token_data = JWTtoken.verify_access_token(token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# Reusable RBAC dependency
def require_roles(*allowed_roles: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403,
                                detail="Insufficient permissions")
        return current_user
    return role_checker
