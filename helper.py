from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from secret import pwd_context
from secret import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from loguru import logger

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
