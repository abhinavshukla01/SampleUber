from fastapi import FastAPI,status, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from auth import get_current_user
from models import User, Login
from database import col
from helper import create_access_token, verify_password, timedelta, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context

router = APIRouter()


@router.post("/create")
def createUser(request:User):
    if request.password != request.confirm_password:
        return {"message" :"Password doesn't match!!"}
    hashedPassword = pwd_context.hash(request.password)
    logger.debug("Password Hashed")
    # newUser = {"username":request.username,
    #             "password":hashedPassword,
    #             "confirm_password":hashedPassword
    #             }
    newUser = request.dict()
    logger.debug("User created")
    col.insert_one(newUser)
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
