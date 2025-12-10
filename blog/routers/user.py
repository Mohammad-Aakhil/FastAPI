from fastapi import APIRouter, HTTPException, status, Depends
from .. import database, schemas, models
from sqlalchemy.orm import Session
from ..hashing import Hash
from typing import List


router = APIRouter(
    prefix='/user',
    tags=['Users'])

get_db = database.get_db


@router.post('/', response_model=schemas.showUser)
def create_user(request: schemas.Users, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.argon2(request.password), role=request.role )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.get("/", response_model=List[schemas.showUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users



@router.get('/{id}', response_model=schemas.showUser)
def get_user(id:int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id:-{id} not found')
    return user

