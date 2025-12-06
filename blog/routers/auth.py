from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from ..JWTtoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password")
    access_token = create_access_token(
        data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


