from pydantic import EmailStr
from pydantic.main import BaseModel
from enum import Enum

class BaseUser(BaseModel):
    username: str
    firstName: str
    lastName: str
    mobileNumber: int
    emailId: EmailStr

class BaseDriver(BaseUser):
    vehicleDetails: str
    registrationNumber: str

class BasePassword(BaseModel):
    userId: str
    password: str

class PasswordModel(BaseModel):
    oldPassword:str
    newPassword: str
    confirm_NewPassword: str

class UserType(str, Enum):
    user = "user"
    driver = "driver"