from .user import UserInDB

class DriverInDB(UserInDB):
    vehicleDetails: str
    registrationNumber: str

class Driver(DriverInDB):
    confirmPassword: str