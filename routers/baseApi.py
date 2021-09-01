from loguru import logger
from models.base import UserType, PasswordModel,BaseUser
from fastapi import FastAPI,status, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependencies import getPassword, get_current_user,create_access_token,verify_password
from utils.db import col, passwordCol,driverCol
from datetime import timedelta 
from utils.security import ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context


router = APIRouter(tags=["Base Routes"])


@router.post("/login")
def login(usertype:UserType, request:OAuth2PasswordRequestForm = Depends()):
    if usertype == "user":
        output = col.find_one({"username":request.username})
    elif usertype == "driver":
        output = driverCol.find_one({"username":request.username})
    if not output:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found!", headers={"header":"header"})
    #pwd = passwordCol.find_one({"userId": str(output["_id"])})
    pwd = getPassword(output["_id"])
    logger.debug(pwd)
    logger.debug(output)
    if not verify_password(request.password, pwd):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!", headers={"header":"header"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": output["username"],
                                            "usertype":usertype}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/change-password")
def changePassword(pwd:PasswordModel,username:str):
    if pwd.newPassword != pwd.confirm_NewPassword:
        return {"message" :"Password doesn't match!!"}
    dataInDB = col.find_one({"username":username})
    if not dataInDB:
        return {"message": "User not found"}
    password = getPassword(dataInDB["_id"])
    if not verify_password(pwd.oldPassword, password):
        return{"message":"Old password is incorrect"}
    hashedPassword = pwd_context.hash(pwd.newPassword)
    up = passwordCol.update({"userId":str(dataInDB["_id"])}, {"$set":{"password":hashedPassword}})
    if up:
        return {"message": up}

@router.get("/me")
def getDetails(current_user: BaseUser = Depends(get_current_user)):
    return current_user