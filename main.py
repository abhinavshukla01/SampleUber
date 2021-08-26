import routes
from auth import get_current_user
from models import User
from fastapi import FastAPI, Depends


app = FastAPI()

app.include_router(routes.router)

@app.get("/welcome")
def welcome(get_current_user: User = Depends(get_current_user)):
    return {"message": "Welcome to Our App!!"}