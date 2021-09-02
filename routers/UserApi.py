from random import randint
from time import sleep
from bson.objectid import ObjectId
from pydantic.types import ConstrainedBytes
from pymongo.message import _randint
from models.base import BaseUser, PasswordModel
from fastapi import FastAPI,status, Depends, HTTPException, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from pydantic.errors import UrlSchemeError
from dependencies import get_current_user,create_access_token,verify_password
from models.user import BaseUser, UpdateUser, UserInput
from models.base import BasePassword
from utils.db import col, passwordCol,rideCol
from datetime import datetime, timedelta 
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context
import requests
import json

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

@router.get("/search-cab")
def searchCab(username: str, source: str, desitination:str):
    cab = {"distance": randint(2,10),
            "price":randint(50,100),
            "username": username,
            "driver":"d"}
    rideCol.insert_one(cab)
    return {"message": "Success"}