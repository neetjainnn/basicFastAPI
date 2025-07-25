from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal, engine
from app import schemas, models, utils, oauth2

router = APIRouter(
    tags= ['authentication']
)

@router.post('/login', response_model=schemas.Tokens)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db) ):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user :
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail= "Invalid Credentials"
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    access_token = oauth2.create_access_token(data={ "user_id" : user.id})
    
    return {"access_token" : access_token, "token_type" : "bearer"}  






