from pydantic import EmailStr
from .login import Login

class UserInDB(Login):
    firstName: str
    lastName: str
    mobileNumber: str
    emailId: EmailStr

class User(UserInDB):
    confirmPassword: str
