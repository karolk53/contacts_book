from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ContactBase(BaseModel):
    first_name: str = Field(regex="")
    last_name: str = Field(regex="")
    email: EmailStr
    phone_number: str = Field(regex="^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")
    image: Optional[str]


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_staff: bool


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class User(UserBase):
    id: int
    is_active: bool
    contacts: list[Contact] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None