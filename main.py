from fastapi import FastAPI, Depends, Request
from models.user import UserInDB
from routers.UserApi import router as userRouter
from routers.DriverApi import router as driverRouter
from dependencies import get_current_user#,temp

app = FastAPI(title="Sample Uber")
app.include_router(userRouter)
app.include_router(driverRouter)

@app.get("/", tags="Welcome")
def welcome(request: Request):
    url = app.url_path_for("register")
    return {"message": url}
