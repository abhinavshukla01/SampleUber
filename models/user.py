from pydantic.main import BaseModel
from models.base import BaseUser
from pydantic import EmailStr


class UserInput(BaseUser):
    password: str
    confirmPassword: str

class UpdateUser(BaseModel):
    firstName: str = "string"
    lastName: str = "string"
    mobileNumber: int = 9999999999
    emailId: EmailStr = "user@example.com"