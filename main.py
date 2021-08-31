from fastapi import FastAPI, Depends
from models.user import UserInDB
from routers.UserApi import router as userRouter
from routers.DriverApi import router as driverRouter
from dependencies import get_current_user


app = FastAPI(title="Sample Uber")
app.include_router(userRouter)
app.include_router(driverRouter)


@app.get("/", tags=["Welcome"])
def welcome(get_user:str = Depends(get_current_user)):
    return {"message": "Welcome to our app!!"}
