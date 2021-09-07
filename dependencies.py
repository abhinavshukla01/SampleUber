from datetime import datetime, timedelta
from models.base import BaseDriver, BaseUser, UserType
from typing import Optional
from jose import JWTError, jwt
from utils.security import ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,pwd_context,SECRET_KEY
from loguru import logger
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from utils.token import Token,TokenData
from utils.db import driverCol, col, passwordCol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/change-password")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        usertype: UserType = payload.get("usertype")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if usertype.value == "driver":
       user = driverCol.find_one({"username":token_data.username})
       data = BaseDriver(**user)
    elif usertype.value == "driver":
        user = col.find_one({"username":token_data.username})
        data = BaseUser(**user)
    if data is None:
        raise credentials_exception
    return data

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    logger.debug("Create Access Token Function called")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    logger.debug("Password verified")
    return pwd_context.verify(plain_password, hashed_password)


def getPassword(userid):
    pwd = passwordCol.find_one({"userId": str(userid)})
    return pwd["password"]


def addTimeStamp(obj: dict):
    obj["lastModified"]=datetime.now()
    if "createdOn" not in obj.keys():
        obj["createdOn"]=obj["lastModified"]
    return obj