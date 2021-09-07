from pydantic import EmailStr
from pydantic.main import BaseModel
from enum import Enum
from datetime import time

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

class RideStatus(str, Enum):
    RIDE_REQUESTED = "RIDE_REQUESTED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DRIVER_DECLINED = "DRIVER_DECLINED"
    USER_DECLINED = "USER_DECLINED"

class RideInput(BaseModel):
    userId: str
    sourceLocation: str
    destinationLocation: str

class RideHistory(BaseModel):
    sourceLocation: str
    destinationLocation: str
    fare: float = 0.0
    startTime: time = None
    endTime: time = None
    distance: float = 0.0
    otp: int = None
    status: RideStatus = None

class Rides():
    rideId: str
    userId: str
    driverId: str = None

class Ratings():
    rideId: str
    driverRating: int
    userRating: int