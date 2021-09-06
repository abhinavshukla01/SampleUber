import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["SampleUber"]
col = db["User"]
driverCol=db["User_Driver"]
passwordCol = db["PasswordCollection"]
rideHistoryCol = db["RideHistory"]
rideCol = db["Rides"]