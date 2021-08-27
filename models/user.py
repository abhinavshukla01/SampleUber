from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    fullName: str
    mobile: int 
    email:  EmailStr
    username: str
    password:str

class UserIn(User):
    confirm_password: str

class UserInDB(User):
    pass