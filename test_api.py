
import requests

data = {
    "name": "Samantha",
    "price": 100,
    "is_offer": True,
}
url = "http://127.0.0.1:8000/items/2"
url ="https://www.uvicorn.org/"
response = requests.put(url)
print(response.text)
