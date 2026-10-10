import json
from http.client import responses
from pprint import pprint

import requests, json
paths = requests.get("http://127.0.0.1:8000/openapi.json").json()["paths"]
print(json.dumps(list(paths.keys()), indent=2))

url = "http://127.0.0.1:8000"
# "item_id":'4e678355-7cbd-4da6-a8b2-7856703563e5'

# response = requests.post(url+"/basket/item/save", json={"id_user":"2","id_item":"1","count":1})

admin = {
  "credentials": {
    "username": "1",
    "password": "1",
    "admin": True
  },
  "title": "1",
  "description": "1",
  "price": 1
}
item = {'items': [{'description': '1',
            'item_id': '2fd207f6-f0e6-420f-874e-3be07d820a8e',
            'price': 1,
            'title': '1'}]}
anonim_basket = 'cac0dece-b78f-4d45-a310-c44582f8359f'
email="супер почта"

# получить все корзины
# response = requests.get(url+"/baskets")
# pprint(response.json())

# # создать карзину
# response = requests.post(url+"/basket/create")
# pprint(response.json())

# # добавить вещь в корзину
# response = requests.post(url+"/basket/item/add", json={"id_item":'2fd707f6-f0e6-420f-874e-3b907d820a8e', "id_basket":anonim_basket, "count":3})
# pprint(response.json())

# показать содержимое корзины
# response = requests.get(url+"/basket", params={"id_basket": anonim_basket})
# pprint(response.json())

# удалить вещь из корзины
# response = requests.delete(url+"/basket/item/delete", json={"id_item":'2fd707f6-f0e6-420f-874e-3b907d820a8e', "id_basket":anonim_basket})

# удалить корзину
# response = requests.delete(url+"/basket/delete", params={"id_basket": anonim_basket})

# зарегистрироваться для заказа
# response = requests.post(url+"/register", json={"email": "супер почта"} )
# print(response.json())

# заказать
response = requests.post(url+"/basket/order", json={"email":email, "id_basket":anonim_basket})
print(response.json())

# получить пользователей
# response = requests.get(url+"/users")
# print(response.json())
