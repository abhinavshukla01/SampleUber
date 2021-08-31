from pydantic import EmailStr
from .login import Login

<<<<<<< HEAD
class UserInDB(Login):
    firstName: str
    lastName: str
    mobileNumber: str
    emailId: EmailStr

class User(UserInDB):
    confirmPassword: str
=======
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
>>>>>>> 80ffbe90bd239538b9c647ab2328d3e188451168
