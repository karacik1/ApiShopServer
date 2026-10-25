import json
from http.client import responses
from pprint import pprint

import requests, json
# paths = requests.get("http://127.0.0.1:8000/openapi.json").json()["paths"]
# print(json.dumps(list(paths.keys()), indent=2))

url = "https://bestjaboashop.onrender.com"
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
item = {
            'description': 'description',
            'price': 1,
            'title': 'new_item213'}

login = {"username":"manager_username","password":"123","admin":True}
anonim_basket = 'f1311287-ffef-4692-a3c9-10b54b3dc238'
email="новая почта"

user='{"id":"uniq_admin_id","email":"manager_email","username":"manager_username","password":"23","admin":false}'


item_in_bd = {"id":"8387ef52-fc99-4321-bc3c-69d28047d00c","title":"new_item213","description":"description","price":1}
# -----------------------ITEMS
# поменять цену
# response = requests.post(url+"/item/change/price", json={"data":{"id_item":"8387ef52-fc99-4321-bc3c-69d28047d00c","new_price":1232222 }, "credentials":login})


# поменять описание
# response = requests.post(url+"/item/change/description", json={"data":{"id_item":"8387ef52-fc99-4321-bc3c-69d28047d00c","new_description":"12222222" }, "credentials":login})

# создать вещь
# response = requests.post(url+"/item/create", json={"item":item, "credentials":login})
# pprint(response.json())

# получить все вещи
# response = requests.get(url+"/items")
# print(response.text)




# -----------------------------BASKETS
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





# ----------------------USERS
# зарегистрироваться для заказа
# response = requests.post(url+"/register", params={"email": "супер новая почта"} )
# print(response.json())

# получить пользователей
# response = requests.get(url+"/users", params=login)
# pprint(response.text)

# заказать
# response = requests.post(url+"/basket/order", json={"email": email, "id_basket": anonim_basket})
# print(response.text)