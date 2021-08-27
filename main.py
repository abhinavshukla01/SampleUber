import routes
import driver
from auth import get_current_user
from models.user import User
from fastapi import FastAPI, Depends


app = FastAPI()

app.include_router(routes.router)
app.include_router(driver.router)

@app.get("/")
def welcome():
    return {"message": "Welcome to Our App!!"}