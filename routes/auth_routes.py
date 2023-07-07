from fastapi import APIRouter, HTTPException,status
from fastapi.encoders import jsonable_encoder
from schemas import UserCreate, User, UserBase
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import Depends
from models import User as UserModel
from authenticate import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


auth_router = APIRouter(
    prefix="/auth",
    tags=["AUTH"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, summary="User registration")
async def signup(user: UserCreate, db: Session = Depends(get_db)):

    """
    ## User registration endpoint
        This endpoint is to register new user, and it requires following:
            - username: string
            - email: string
            - is_staff: boolean
            - password: string
    """

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


@auth_router.post("/token")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

    """
        ## Get token
        This is endpoint to get the JWT token for the user
    """

    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.username},expires_delta=token_expires)

    return {"access_token": token, "token_type": "bearer"}


@auth_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
        ## User info
        On this endpoint you can get info about authenticated user
    """

    return jsonable_encoder(current_user)


@auth_router.get("/users/all")
async def get_all_users(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
        ## Users list
        Endpoint that allows to get list of all users but only for staff users.
     """

    if current_user.is_staff:
        return jsonable_encoder(db.query(UserModel).all())

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You dont have permissions!")