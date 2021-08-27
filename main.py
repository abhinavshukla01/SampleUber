import routes
import driver
from fastapi import FastAPI


app = FastAPI(title="SampleUber")

app.include_router(routes.router)
app.include_router(driver.router)

@app.get("/", tags=["Welcome"])
def welcome():
    return {"message": "Welcome to Our App!!"}


