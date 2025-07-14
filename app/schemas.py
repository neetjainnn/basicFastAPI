from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ===========================
# User Schemas
# ===========================

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ===========================
# Post Schemas
# ===========================

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    post: PostResponse
    votes: int

    class Config:
        from_attributes = True


# ===========================
# Token Schemas
# ===========================

class Tokens(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: Optional[str]


# ===========================
# Vote Schema
# ===========================

class Votes(BaseModel):
    post_id: int
    dir: int
