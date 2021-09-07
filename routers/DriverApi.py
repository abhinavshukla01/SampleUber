from models.base import RideHistory
from typing import Optional
from fastapi import status, Depends, HTTPException, APIRouter, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Body
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from models.driver import DriverInput
from models.base import BasePassword, BaseDriver, AcceptDecline
from utils.db import driverCol, passwordCol,rideCol,rideHistoryCol
from dependencies import get_current_user,create_access_token,verify_password
from datetime import datetime, timedelta
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS, loads
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
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
    insertId = driverCol.insert_one(newUser.dict()).inserted_id
    logger.debug(type(insertId))
    hashedPassword = pwd_context.hash(request.password)
    logger.debug("Password hashed and inserted in DB")
    newPassword = BasePassword(**{"userId":str(insertId),
                                "password":hashedPassword})
    passwordCol.insert_one(newPassword.dict())
    return {"message": "User Created Successfully"}


@router.get("/ride-requests")
def rideRequests(username:str):
    driverId = str(driverCol.find_one({"username":username})["_id"])
    #driverId=""
    rideIds = rideCol.find({"driverId":driverId})
    op=[]
    for ride in rideIds:
        req = rideHistoryCol.find_one({"_id":ObjectId(ride["rideId"])})
        #logger.debug(req)
        req["_id"]=str(req["_id"])
        op.append(req)
    return op
    # list_cur = list(req)
    # for i in list_cur:
    #     i["_id"]=str(i["_id"])
    # json_data = dumps(list_cur)
    # return loads(json_data)


@router.get("/accept-request")
def acceptRequest(rideId: str,status : AcceptDecline):
    if status == "ACCEPTED":
        totp = pyotp.TOTP('base32secret3232')
        otp = totp.now()
        rideHistoryCol.update({"_id":ObjectId(rideId)}, {"$set":{"otp":int(otp),"status":"ACCEPTED"}})
    elif status == "DECLINED":
        up=rideHistoryCol.update({"_id":ObjectId(rideId)}, {"$set":{"status":"DRIVER_DECLINED"}})
    
    pag.alert(text=status.value)
    return {"message": "Updated"}
    #alert(text='', title='', button='OK')
    # otp_in = pag.prompt('Enter OTP')
    # return {"status": "Accepted","otp verified": otp==otp_in}
    # return {"status": "Declined by driver"}

@router.patch("/start-ride")
def startRide(otp: int, rideId: str):
    req = rideHistoryCol.find_one({"_id":ObjectId(rideId)})
    if otp == req["otp"]:
        up = rideHistoryCol.update({"_id":ObjectId(rideId)},{"$set":{"status":"IN_PROGRESS","startTime":datetime.now()}})
        return up 
    else:
        return {"message": "Incorrect OTP"}

@router.patch("/end-ride")
def startRide(rideId: str):
    req = rideHistoryCol.find_one({"_id":ObjectId(rideId)})
    up = rideHistoryCol.update({"_id":ObjectId(rideId)},{"$set":{"status":"COMPLETED","endTime":datetime.now()}})
    return up 
    

