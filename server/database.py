import threading
from pymongo import MongoClient
client = MongoClient("localhost", 12345)

class Database:

    def __init__(self):

        db = client["app-database-1"]
        self.users = db["users"]

        self.mutex = threading.Lock()


    def addUser(self, username, pw_salt, pw_hash):

        userdata = {
            "username": username,
            "pw_hash": pw_hash,
            "pw_salt": pw_salt,
            "texts": []
        }
    
        self.mutex.acquire()
        if self.users.find({"username": username}).count() == 0:
            self.users.insert_one(userdata)
        self.mutex.release()

        print("Successful addUser")


    def addText(self, username, json):

        # Check that the username exists
        self.mutex.acquire()
        user = self.users.find_one({"username": username})
        if user != None:
            self.users.update(user, {"$push": {"texts": json}})
        self.mutex.release()


    def getTexts(self, username):
        
        output = None

        # Get all texts that ever existed
        self.mutex.acquire()
        user = self.users.find_one({"username": username})
        if user != None:
            output = user["texts"]
        self.mutex.release()

        return output
