from calendar import day_abbr
from fastapi import FastAPI,status, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from pydantic.errors import UrlSchemeError
from dependencies import get_current_user,create_access_token,verify_password
from models.user import User,UserInDB, PasswordModel
from utils.db import col
from datetime import datetime, timedelta 
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context

router = APIRouter(prefix="/user",tags=["User"])

@router.post("/register")
def register(request:User):
    username_in_db = col.find_one({"username":request.username})
    if username_in_db:
        return {"message" : "Username is already taken!!"}
    if request.password != request.confirmPassword:
        return {"message" :"Password doesn't match!!"}
    hashedPassword = pwd_context.hash(request.password)
    logger.debug("Password Hashed")
    request.password=hashedPassword
    newUser=UserInDB(**request.dict())
    logger.debug("User created")
    col.insert_one(newUser.dict())
    logger.debug("User Inserted in DB")
    return {"message": "User Created Successfully"}


@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends()):
    output = col.find_one({"username":request.username})
    if not output:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!", headers={"header":"header"})
    if not verify_password(request.password, output["password"]):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!", headers={"header":"header"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": output["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}            


# @router.patch("/update-user/{username}")
# def updateUser(username:str, user:User):
#     logger.debug("Inside update User function")
#     hashedPassword = pwd_context.hash(user.password)
#     user.password = hashedPassword
#     user.confirmPassword = hashedPassword
#     dataInDb = col.find_one_and_update({"username":username}, {"$set":dict(user)})
#     logger.debug("data fetched")
#     return {"message": dataInDb["username"] + " is updated"}

@router.put("/change-password")
def changePassword(pwd:PasswordModel,username:str):
    if pwd.newPassword != pwd.confirm_NewPassword:
        return {"message" :"Password doesn't match!!"}
    dataInDB = col.find_one({"username":username})
    if not dataInDB:
        return {"message": "User not found"}
    if not verify_password(pwd.oldPassword, dataInDB["password"]):
        return{"message":"Old password is incorrect"}
    hashedPassword = pwd_context.hash(pwd.newPassword)
    up = col.update({"username":username}, {"$set":{"password":hashedPassword}})
    if up:
        return {"message": up}