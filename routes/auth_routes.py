from fastapi import APIRouter, HTTPException,status
from fastapi.encoders import jsonable_encoder
from schemas import UserCreate, User
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import Depends
from models import User as UserModel
from authenticate import *


auth_router = APIRouter(
    prefix="/auth",
    tags=["AUTH"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_username = db.query(UserModel).filter(UserModel.username == user.username).first()
    if user_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that username already exists!")

    user_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if user_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that email already exists!")

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        is_staff=user.is_staff
    )

    db.add(new_user)
    db.commit()

    return jsonable_encoder(new_user)