from fastapi import FastAPI, Response, status, HTTPException, Depends

from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List

import time

from app import models
from app import database
from app.database import get_db, SessionLocal, engine

from routers import post,user, auth, vote

models.Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session




# for render 
import os

# Dynamically load config and database modules based on environment
if os.getenv("RENDER_DEPLOY") == "true":
    from render import config, database
else:
    from app import config, database




app = FastAPI()

origins = ["*"]  #here we put all the domains from where we are supposed to fetch the data 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts