from pydantic.main import BaseModel
from .base import RideStatus

class RideOutput(BaseModel):
    sourceLocation: str
    destinationLocation: str
    fare: float = 0.0
    distance: float = 0.0
    otp: int = None
    status: RideStatus = None
    name: str
    mobileNumber: int
    vehicleDetails: str
    registrationNumber: str
