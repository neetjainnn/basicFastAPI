from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    curr_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = (
        db.query(models.Posts, func.count(models.Votes.post_id).label('votes'))
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)
        .filter(models.Posts.title.contains(search))
        .group_by(models.Posts.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return [{"post": post, "votes": votes} for post, votes in results]


import traceback

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), curr_user: models.Users = Depends(oauth2.get_current_user)):
    try:
        new_post = models.Posts(
            title=post.title,
            content=post.content,
            published=post.published,
            user_id=curr_user.id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        print("Error in create_post:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error: " + str(e))


@router.get("/latest", response_model=schemas.PostResponse)
def latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Posts).order_by(models.Posts.id.desc()).first()
    if not post:
        raise HTTPException(status_code=404, detail="No posts found")
    return post


from sqlalchemy import func

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_with_votes = (
        db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)
        .filter(models.Posts.id == id)
        .group_by(models.Posts.id)
        .first()
    )

    if not post_with_votes:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    post, votes = post_with_votes
    return {"post": post, "votes": votes}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    db_post = post_query.first()

    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    if db_post.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
