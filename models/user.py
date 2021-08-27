from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    username: str
    password: str

class User(BaseModel):
    fullName: str
    mobile:  str
    email:  EmailStr
    username: str
    password:str
    confirm_password: str

class DriverInDB(BaseModel):
    fullName: str
    mobile:  str
    email:  EmailStr
    username: str
    password:str
    vehicleDetails: str
    registrationNumber: str

class Driver(DriverInDB):
    confirmPassword: str
