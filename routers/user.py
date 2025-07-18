from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, utils

from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):

    hashed_pasword = utils.hash(user.password)
    user.password = hashed_pasword

    new_user = models.Users(password = user.password, email = user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={id} not found"
        )
    return user