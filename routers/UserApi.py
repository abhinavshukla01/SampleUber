from models.base import RideHistory, RideInput, BaseUser, PasswordModel, BasePassword
from models.user import BaseUser, UpdateUser, UserInput
from time import sleep
from fastapi import FastAPI,status, Depends, HTTPException, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from pydantic.errors import UrlSchemeError
from dependencies import get_current_user,create_access_token,verify_password
from utils.db import col, passwordCol, rideCol, rideHistoryCol
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context
import random

router = APIRouter(prefix="/user",tags=["User"])

@router.post("/register")
def register(request:UserInput):
    username_in_db = col.find_one({"username":request.username})
    if username_in_db:
        return {"message" : "Username is already taken!!"}
    if request.password != request.confirmPassword:
        return {"message" :"Password doesn't match!!"}
    if len(str(request.mobileNumber)) != 10:
        return {"message" : "Mobile number is invalid, it should contain 10 characters"}
    newUser = BaseUser(**request.dict())
    insertId = col.insert_one(newUser.dict()).inserted_id
    logger.debug(type(insertId))
    hashedPassword = pwd_context.hash(request.password)
    logger.debug("Password hashed and inserted in DB")
    newPassword = BasePassword(**{"userId":str(insertId),
                                "password":hashedPassword})
    passwordCol.insert_one(newPassword.dict())
    return {"message": "User Created Successfully"}
   
           


@router.patch("/update-user/{username}")
def updateUser(username:str, user:UpdateUser):
    dataInDB = col.find_one({"username":username})   
    if len(str(user.mobileNumber)) != 10:
        return {"message" : "Mobile number is invalid, it should contain 10 characters"}
    update_status = col.update({"username":username},
     {"$set":{  "firstName":user.firstName,
                "lastName":user.lastName,
                "mobileNumber":user.mobileNumber,
                "emailId":user.emailId 
            }})
    if update_status:
        return {"message": update_status}

@router.post("/search-cab")
def searchCab(request: RideInput):
    userId = str(col.find_one({"username":request.userId})["_id"])
    rideRequest=RideHistory(**request.dict())
    rideRequest.userId=userId
    rideRequest.driverId='d'
    rideRequest.distance=round(random.random()*10,2)
    rideRequest.fare=round(random.random()*100,2)
    rideRequest.status="RIDE_REQUESTED"
    ride_id = rideHistoryCol.insert_one(rideRequest.dict()).inserted_id
    ride={"rideId":str(ride_id), "userId":userId, "driverId":rideRequest.driverId}
    rideCol.insert_one(ride)
    return {"message": "Success"}