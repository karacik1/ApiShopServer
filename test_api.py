import json
from pprint import pprint

import requests, json
paths = requests.get("http://127.0.0.1:8000/openapi.json").json()["paths"]
print(json.dumps(list(paths.keys()), indent=2))

url = "http://127.0.0.1:8000"
# "item_id":'4e678355-7cbd-4da6-a8b2-7856703563e5'

# response = requests.post(url+"/basket/item/save", json={"id_user":"2","id_item":"1","count":1})
#



response= requests.post(url+"/item/create", json={
  "credentials": {
    "username": "1",
    "password": "1",
    "admin": True
  },
  "title": "1",
  "description": "1",
  "price": 1
})
print(response.text)


response= requests.get(url+"/items")
pprint(response.json())


