# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H5XebaEN5X8tDv-HajT4P4Zwt_xzdWgK

FastAPI and PostgreSQL
"""

pip install fastapi uvicorn sqlalchemy psycopg2 pydantic python-multipart python-dotenv

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from .config import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""User Management"""

from sqlalchemy import Column, Integer, String
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user_schema import UserCreate
from ..database import get_db

router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

"""Main Application"""

from fastapi import FastAPI
from .routers import users, jobs, iot

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["Users"])
# You can add jobs and iot routers later.

@app.get("/")
def read_root():
    return {"message": "Welcome to PathFinder AI!"}

DATABASE_URL=postgresql://username:password@localhost/pathfinder_db