import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

# ===== ITEMS =====

# def test_get_all_items():
#     """Позитивный тест: получение списка всех товаров."""
#     response = requests.get(f"{BASE_URL}/items")
#     data = response.json()
#     assert "items" in data
#     assert isinstance(data["items"], list)
#
#
# def test_create_item(admin_credentials, new_item_data):
#     """Позитивный тест: создание нового товара."""
#     payload = {
#         "item": new_item_data,
#         "credentials": admin_credentials
#     }
#     response = requests.post(f"{BASE_URL}/item/create", json=payload)
#     assert response.text == '"done"'
#
# def test_change_item_price(admin_credentials, created_item):
#     """Позитивный тест: изменение цены товара."""
#     item_id = created_item["id"]
#     payload = {
#         "data": {"id_item": item_id, "new_price": 999},
#         "credentials": admin_credentials
#     }
#     response = requests.post(f"{BASE_URL}/item/change/price", json=payload)
#     # Дополнительно можно проверить, что цена изменилась
#
#
# def test_change_item_description(admin_credentials, created_item):
#     """Позитивный тест: изменение описания товара."""
#     item_id = created_item["id"]
#     payload = {
#         "data": {"id_item": item_id, "new_description": "Updated Description"},
#         "credentials": admin_credentials
#     }
#     response = requests.post(f"{BASE_URL}/item/change/description", json=payload)
#     assert response.status_code == 200
#
#
# # ===== BASKETS =====
#
# def test_get_all_baskets():
#     """Позитивный тест: получение списка корзин."""
#     response = requests.get(f"{BASE_URL}/baskets")
#
#
# def test_create_basket():
#     """Позитивный тест: создание корзины."""
#     response = requests.post(f"{BASE_URL}/basket/create")
#     assert "id_basket" in response.json()
#
#
# def test_add_item_to_basket(basket_id, created_item):
#     """Позитивный тест: добавление товара в корзину."""
#     item_id = created_item["id"]
#     payload = {"id_item": item_id, "id_basket": basket_id, "count": 2}
#     response = requests.post(f"{BASE_URL}/basket/item/add", json=payload)
#
#
# def test_get_basket_content(basket_id):
#     """Позитивный тест: получение содержимого корзины."""
#     response = requests.get(f"{BASE_URL}/basket", params={"id_basket": basket_id})
#
#
#     # Проверяем, что корзина не пустая (там должен быть наш item)
#     data = response.json()
#     assert "items" in data
#
#
# def test_delete_item_from_basket(basket_id, created_item):
#     """Позитивный тест: удаление товара из корзины."""
#     item_id = created_item["id"]
#     payload = {"id_item": item_id, "id_basket": basket_id}
#     response = requests.delete(f"{BASE_URL}/basket/item/delete", json=payload)
#
#
#
# # ===== USERS & ORDER =====
#
# def test_register_user():
#     """Позитивный тест: регистрация нового пользователя."""
#     email = "test_user_unique@example.com"  # уникальный email для теста
#     # Если ты сделал email через тело:
#     # response = requests.post(f"{BASE_URL}/register", json={"email": email})
#
#     # Если через query-параметр (как в твоем файле):
#     response = requests.post(f"{BASE_URL}/register", params={"email": email})
#
#
#
#
# def test_get_users(admin_credentials):
#     """Позитивный тест: получение списка пользователей."""
#     response = requests.get(f"{BASE_URL}/users", params=admin_credentials)
#
#
#
# def test_order_basket(basket_id):
#     """Позитивный тест: оформление заказа."""
#     # Перед заказом надо добавить что-то в корзину, иначе заказ пустой
#     # Для простоты можно просто дергать заказ, если сервис позволяет
#     payload = {"email": "order_user@example.com", "id_basket": basket_id}
#     response = requests.post(f"{BASE_URL}/basket/order", json=payload)
