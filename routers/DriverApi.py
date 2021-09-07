from hashlib import new
from typing import List
from fastapi import APIRouter, Query
from loguru import logger
from models.driver import DriverInput
from models.base import BasePassword, BaseDriver, RideHistoryOutput
from utils.db import driverCol, passwordCol,rideCol,rideHistoryCol
from dependencies import addTimeStamp
from datetime import datetime
from utils.security import pwd_context
from bson.objectid import ObjectId
import pyotp
import pyautogui as pag

router = APIRouter(prefix="/driver",tags=["Driver"])

@router.post("/register")
def register(request:DriverInput):
    username_in_db = driverCol.find_one({"username":request.username})
    if username_in_db:
        return {"message" : "Username is already taken!!"}
    if request.password != request.confirmPassword:
        return {"message" :"Password doesn't match!!"}
    if len(str(request.mobileNumber)) != 10:
        return {"message" : "Mobile number is invalid, it should contain 10 characters"}
    
    newUser = BaseDriver(**request.dict())
    newUser = addTimeStamp(newUser.dict())
    insertId = driverCol.insert_one(newUser).inserted_id
    logger.debug(type(insertId))
    hashedPassword = pwd_context.hash(request.password)
    logger.debug("Password hashed and inserted in DB")
    newPassword = BasePassword(**{"userId":str(insertId),
                                "password":hashedPassword})
    newPassword=addTimeStamp(newPassword.dict())
    passwordCol.insert_one(newPassword)
    return {"message": "User Created Successfully"}


@router.get("/ride-requests",response_model=List[RideHistoryOutput])
def rideRequests(username:str):
    driverId = str(driverCol.find_one({"username":username})["_id"])
    #driverId=""
    rideIds = rideCol.find({"driverId":driverId})
    op=[]
    for ride in rideIds:
        req = rideHistoryCol.find_one({"_id":ObjectId(ride["rideId"])})
        #logger.debug(req)
        req["rideId"]=str(req["_id"])
        op.append(req)
    return op
    # list_cur = list(req)
    # for i in list_cur:
    #     i["_id"]=str(i["_id"])
    # json_data = dumps(list_cur)
    # return loads(json_data)


@router.get("/accept-request")
def acceptRequest(rideId: str,status : str = Query("...",enum=["ACCEPTED","DECLINED"])):
    if status == "ACCEPTED":
        totp = pyotp.TOTP('base32secret3232')
        otp = totp.now()
        rideHistoryCol.update({"_id":ObjectId(rideId)}, {"$set":{"otp":int(otp),"status":"ACCEPTED","lastModified":datetime.now()}})
    elif status == "DECLINED":
        up=rideHistoryCol.update({"_id":ObjectId(rideId)}, {"$set":{"status":"DRIVER_DECLINED","lastModified":datetime.now()}})
    
    pag.alert(text=status)
    return {"message": "Updated"}
    #alert(text='', title='', button='OK')
    # otp_in = pag.prompt('Enter OTP')
    # return {"status": "Accepted","otp verified": otp==otp_in}
    # return {"status": "Declined by driver"}

@router.patch("/start-ride")
def startRide(otp: int, rideId: str):
    req = rideHistoryCol.find_one({"_id":ObjectId(rideId)})
    if otp == req["otp"]:
        up = rideHistoryCol.update({"_id":ObjectId(rideId)},{"$set":{"status":"IN_PROGRESS","startTime":datetime.now(),"lastModified":datetime.now()}})
        return up 
    else:
        return {"message": "Incorrect OTP"}

@router.patch("/end-ride")
def endRide(rideId: str):
    req = rideHistoryCol.find_one({"_id":ObjectId(rideId)})
    up = rideHistoryCol.update({"_id":ObjectId(rideId)},{"$set":{"status":"COMPLETED","endTime":datetime.now(),"lastModified":datetime.now()}})
    return up 
    

