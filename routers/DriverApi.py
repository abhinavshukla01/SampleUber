from fastapi import status, Depends, HTTPException, APIRouter
from fastapi.param_functions import Body
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from models.driver import DriverInput
from models.base import BasePassword, BaseDriver
from utils.db import driverCol, passwordCol
from dependencies import get_current_user,create_access_token,verify_password
from datetime import datetime, timedelta
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context


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
       
