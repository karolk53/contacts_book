from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas import *
from sqlalchemy.orm import Session
from models import User as UserModel


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password_hash(password_hash: str, plain_password: str):
    return pwd_context.verify(plain_password, password_hash)


def get_user(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username)


def authenticate_user(db: Session,username: str, password: str):
    user = get_user(db=db, username=username)
    if not user:
        return False
    if not verify_password_hash(password_hash=user.password, plain_password=password):
        return False
    return user


