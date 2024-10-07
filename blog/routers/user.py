from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash

router = APIRouter()
getDb = database.getDb


@router.post('/user', response_model=schemas.ShowUser, tags=['users'])
def createUser(request: schemas.User, db: Session = Depends(getDb)):
    newUser = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    email = request.email
    if '@' not in email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please add correct email id")
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def getUser(id: int, db: Session = Depends(getDb)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist")
    return user