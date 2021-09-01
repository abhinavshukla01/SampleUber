from models.base import BaseUser


class UserInput(BaseUser):
    password: str
    confirmPassword: str

class UpdateUser(BaseUser):
    pass