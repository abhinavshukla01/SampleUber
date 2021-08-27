import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TodoList"]
col = db["SampleUber"]
driverCol=db["User_Driver"]