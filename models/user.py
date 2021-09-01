from pydantic import EmailStr
from pydantic.main import BaseModel
from .login import Login

class UserInDB(Login):
    firstName: str
    lastName: str
    mobileNumber: int
    emailId: EmailStr

class User(UserInDB):
    confirmPassword: str

class PasswordModel(BaseModel):
    oldPassword: str
    newPassword: str
    confirm_NewPassword: str