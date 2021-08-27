from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.param_functions import Body
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from models.user import Driver, DriverInDB
from database import driverCol
from helper import create_access_token, verify_password, timedelta, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context

router = APIRouter(prefix="/driver",tags=["Driver"])


@router.post("/register")
def register(*,request:Driver):
    username_in_db = driverCol.find_one({"username":request.username})
    if username_in_db:
        return {"message" : "Username is already taken!!"}
    if request.password != request.confirmPassword:
        return {"message" :"Password doesn't match!!"}
    if len(request.registrationNumber) != 10:
        return {"message" : "Registration number is invalid, if should contain 10 characters"}
    hashedPassword = pwd_context.hash(request.password)
    request.password = hashedPassword
    logger.debug("Password Hashed")
    driverInDB=DriverInDB(**request.dict())
    driverCol.insert_one(driverInDB.dict())
    logger.debug("User Inserted in DB")
    return {"message": "User Created Successfully"}


@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends()):
    output = driverCol.find_one({"username":request.username})
    if not output:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!", headers={"header":"header"})
    if not verify_password(request.password, output["password"]):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!", headers={"header":"header"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": output["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}            
