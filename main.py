from models.user import User
from fastapi.param_functions import Depends
import routes
import driver
from fastapi import FastAPI
from auth import get_current_user

app = FastAPI(title="SampleUber")

app.include_router(routes.router)
app.include_router(driver.router)

@app.get("/", tags=["Welcome"])
def welcome(get_current_user:User = Depends(get_current_user)):
    return {"message": "Welcome to Our App!!"}

