from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)
    is_active = Column(String, default=True)

    contacts = relationship("Contact", back_populates="user")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String)
    image = Column(String, nullable=True)  #IT IS ADDED BUT FOR NOW UNSUPPORTED
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="contacts")