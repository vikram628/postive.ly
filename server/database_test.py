from pymongo import MongoClient
client = MongoClient("localhost", 12345)

db = client["test-database"]

userdata = {
        "username": "dwinkelman0",
        "password": "12345r6",
        "texts": []
}

users = db["users"]

users.insert_one(userdata)

#print(users.find_one({"username": "dwinkelman0"}))
#print(users.find_one({"username": "nope"}))

user = users.find_one({"username": "dwinkelman0"})

message = {
        "original": "hey wya",
        "score": 0.4534,
        "timestamp": 1234,
        "id": 0
}

#users.update(user, {"$push": {"texts": message}})

#print(user["texts"])
texts = users.find({"username": "dwinkelman0", "texts": {"timestamp": {"$lte": 2000}}})
for text in list(texts):
    print(text["original"])

