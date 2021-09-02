from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Body
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from models.driver import DriverInput
from models.base import BasePassword, BaseDriver
from utils.db import driverCol, passwordCol,rideCol
from dependencies import get_current_user,create_access_token,verify_password
from datetime import datetime, timedelta
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context
from bson.json_util import dumps, loads, CANONICAL_JSON_OPTIONS
from fastapi.responses import JSONResponse
import re

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
       
@router.get("/all-requests")
def allRequests():
    req = rideCol.find({})
    list_cur = list(req)
    json_data = dumps(list_cur)
    return loads(json_data)