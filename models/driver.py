from models.base import BaseDriver


class DriverInput(BaseDriver):
    password: str
    confirmPassword: str

class UpdateDriver(BaseDriver):
    pass