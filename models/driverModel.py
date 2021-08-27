from pydantic import BaseModel, EmailStr

class DriverInDB(BaseModel):
    fullName: str
    mobile:  str
    email:  EmailStr
    username: str
    password:str
    vehicleDetails: str
    registrationNumber: str

class Driver(DriverInDB):
    confirmPassword: str