from models.response import RideOutput
from models.base import RideHistory, RideInput, BaseUser, PasswordModel, BasePassword
from models.user import BaseUser, UpdateUser, UserInput
from time import sleep
from fastapi import FastAPI,status, Depends, HTTPException, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from pydantic.errors import UrlSchemeError
from dependencies import get_current_user,create_access_token,verify_password
from utils.db import col, passwordCol, rideCol, rideHistoryCol, driverCol
from bson.objectid import ObjectId
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context
import random
from typing import List

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
    driverId = "6136fe9bc7a31561eae58e16"
    rideRequest=RideHistory(**request.dict())
    #rideRequest.userId=userId
    #rideRequest.driverId='d'
    rideRequest.distance=round(random.random()*10,2)
    rideRequest.fare=round(random.random()*100,2)
    rideRequest.status="RIDE_REQUESTED"
    ride_id = rideHistoryCol.insert_one(rideRequest.dict()).inserted_id
    ride={"rideId":str(ride_id), "userId":userId, "driverId":driverId}
    rideCol.insert_one(ride)
    return {"message": "Success"}

# @router.get("/ride-requests")
# def rideRequests(username:str):
#     userId = str(col.find_one({"username":username})["_id"])
#     #driverId=""
#     rideIds = rideCol.find({"userId":userId})
#     op=[]
#     for ride in rideIds:
#         req = rideHistoryCol.find_one({"_id":ObjectId(ride["rideId"])})
#         #logger.debug(req)
#         req["_id"]=str(req["_id"])
#         op.append(req)
#     return op

@router.get("/user-requests-status")
def userRequestStatus(rideId:str):
    #driverId = str(driverCol.find_one({"username":username})["_id"])
    #userId = str(col.find_one({"username":username})["_id"])
    #rideIds = rideCol.find({"userId":userId})
    rideIds = rideCol.find({"rideId":rideId})
    op=[]
    for ride in rideIds:
        req = rideHistoryCol.find_one({"_id":ObjectId(ride["rideId"])})
        if req["status"]=="ACCEPTED" or req["status"]=="IN_PROGRESS":
            #driverId=ride["driverId"]
            driverDetails=driverCol.find_one({"_id":ObjectId(ride["driverId"])})
            #logger.debug(req)
            #req["_id"]=str(req["_id"])
            driverDetails["name"]=driverDetails["firstName"]+" "+driverDetails["lastName"]
            req.update(driverDetails)
            rideDetails = RideOutput(**req)
            op.append(rideDetails)
        #rideDetails.name=req.update(driverDetails)
        elif req["status"]=="RIDE_REQUESTED" or req["status"]=="DRIVER_DECLINED":
            rideDetails=dict()
            rideDetails["sourceLocation"]=req["sourceLocation"]
            rideDetails["destinationLocation"]=req["destinationLocation"]
            rideDetails["status"]=req["status"]
            op.append(rideDetails)
    return op