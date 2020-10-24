import requests
import json
from datetime import datetime

headers = {"Content-type": "application/json", "Accept": "text/plain"}

def addUser():
    url = "http://10.194.223.134:5000/add_user"
    data = {"username": "test_user"}
    requests.post(url, data=json.dumps(data), headers=headers)

def addMessage():
    url = "http://10.194.223.134:5000/phone_data/test_user"
    data = {"message": "My Sample Message", "timestamp": datetime.timestamp(datetime.now())}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.json())

addUser()
addMessage()
