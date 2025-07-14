from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal, engine
from app import schemas, models, utils, oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Votes, db: Session = Depends(get_db), curr_user: models.Users = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,
        models.Votes.user_id == curr_user.id
    )
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found")
    
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {curr_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Votes(post_id=vote.post_id, user_id=curr_user.id)  
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}