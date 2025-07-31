from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import models, schemas, utils

from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)


from sqlalchemy.exc import IntegrityError

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(password=user.password, email=user.email)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error during user creation")
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={id} not found"
        )
    return user