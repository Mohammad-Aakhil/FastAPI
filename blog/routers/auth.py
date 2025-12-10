from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from ..JWTtoken import create_access_token, create_refresh_token, verify_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db

# @router.post('/login')
# def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.name == request.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Invalid Credentials")
#     if not Hash.verify(user.password, request.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Incorrect Password")
#     access_token = create_access_token(
#         data={"sub": user.name, "role": user.role})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.name == request.username).first()

    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id, "role": user.role})
    refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(refresh_token: str):
    user_id, role = verify_refresh_token(refresh_token)
    access_token = create_access_token({"user_id": user_id, "role": role})
    return {"access_token": access_token, "token_type": "bearer"}
