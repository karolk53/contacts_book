from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ContactBase(BaseModel):
    first_name: str = Field(regex="^[a-zA-Z]{2,50}")
    last_name: str = Field(regex="^[a-zA-Z]{2,50}")
    email: EmailStr
    phone_number: str = Field(regex="^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3}$")
    image: Optional[str]


class ContactCreate(ContactBase):
    class Config:
        schema_extra = {
            "example":  {
                    "first_name": "Julia",
                    "last_name": "Nowak",
                    "email": "julianowak@example.com",
                    "phone_number": "786-307-361",
                    "image": "string"
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "username": "johnsmith",
                "email": "johnsmith@example.com",
                "is_staff": True,
                "password": "password"
            }
        }


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