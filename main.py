from fastapi import FastAPI
from routers.UserApi import router as userRouter
from routers.DriverApi import router as driverRouter
from routers.baseApi import router as baseRouter

app = FastAPI(title="Sample Uber")
app.include_router(baseRouter)
app.include_router(userRouter)
app.include_router(driverRouter)

@app.get("/", tags=["Welcome"])
def welcome():
    return {"message": "Welcome to our app!!"}
