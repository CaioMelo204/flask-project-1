import requests

BASE = "http://localhost:5000/"

response = requests.put(BASE + "video/2", {
    "likes": 10,
    "name": "test",
    "views": 10,
})
print(response.json())

input()

response = requests.get(BASE + "video/2")
print(response.json())
