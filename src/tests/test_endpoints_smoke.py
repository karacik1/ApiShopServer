from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from blog.domains import Basket, BasketItem
from blog.main import app
from blog.schemas import ChangeItemDescriptionModel, ChangeItemPriceModel

client = TestClient(app)


# ---------------ENDPOINTS
# ---------------GET
class GetEndpoint:
    url = None
    response_type = None
    status_code = None
    data_correct = {}
    data_404 = {}
    data_422 = {
        "unreal_param": True
    }

    @pytest.mark.smoke
    def test_endpoint_positive_contract(self):
        response = client.get(url=self.url, params=self.data_correct)

        # Сразу проверяем и статус, и структуру ответа
        assert response.status_code == self.status_code
        assert isinstance(response.json(), self.response_type)

    @pytest.mark.smoke
    def test_param_is_not_exists(self):
        response = client.get(url=self.url, params=self.data_422)
        assert response.status_code == 422


class TestEndPointGetUsers(GetEndpoint):
    url = "/users"
    response_type = dict
    status_code = 200
    data_404 = {
        "id": "unreal_id"
    }


class TestEndPointGetBaskets(GetEndpoint):
    url = "/baskets"
    response_type = dict
    status_code = 200
    data_404 = {
        "id_basket": "unreal_id"
    }


class TestEndPointGetItems(GetEndpoint):
    url = "/items"
    response_type = dict
    status_code = 200
    data_404 = {
        "id": "unreal_id"
    }


# ---------------POST
class PostEndpoint:
    url = None
    response_type = None
    status_code = None
    data_correct = {}
    data_422 = {
        "unreal_param": True
    }
    response = None
    mok = None

    def test_endpoint_positive_contract(self):
        response = client.post(url=self.url, json=self.data_correct)

        # Сразу проверяем и статус, и структуру ответа
        assert response.status_code == self.status_code

    def test_param_is_not_exists(self):
        response = client.post(url=self.url, json=self.data_422)
        assert response.status_code == 422


class TestEndPointCreateBasket:
    url = "/basket/create"
    response_type = str
    status_code = 201

    @pytest.mark.smoke
    def test_endpoint_positive_contract(self):
        response = client.post(url=self.url)

        # Сразу проверяем и статус, и структуру ответа
        assert response.status_code == self.status_code


class TestEndpointOrderBasket(PostEndpoint):
    url = "/basket/order"
    response_type = str
    status_code = 201
    data_correct = {"email": "email1",
                    "id_basket": "1", }

    @pytest.mark.smoke
    @patch("blog.services.order_basket")
    def test_endpoint_positive_contract(self, mok_service):
        mok_service.return_value = "Done"
        super().test_endpoint_positive_contract()


# ----------------DELETE
class DeleteEndpoint:
    url = None
    response_type = None
    status_code = None
    data_correct = {}
    data_422 = {
        "unreal_param": True
    }
    response = None
    mok = None

    @pytest.mark.smoke
    def test_endpoint_positive_contract(self):
        response = client.delete(url=self.url, params=self.data_correct)

        # Сразу проверяем и статус, и структуру ответа
        assert response.status_code == self.status_code

    @pytest.mark.smoke
    def test_param_is_not_exists(self):
        response = client.delete(url=self.url, params=self.data_422)
        assert response.status_code == 422


class TestEndPointDeleteBasket(DeleteEndpoint):
    url = "/basket/delete"
    status_code = 204
    data_correct = {
        "id_basket": "5",
    }

    @patch("blog.services.delete_basket")
    def test_endpoint_positive_contract(self, mok):
        mok.return_value = None
        super().test_endpoint_positive_contract()


class TestEndPointDeleteBasketItem(DeleteEndpoint):
    url = "/basket/item/delete"
    status_code = 204
    data_correct = {
        "id_basket": "5",
        "id_item": "1"
    }

    @patch("blog.services.delete_item")
    def test_endpoint_positive_contract(self, mok):
        mok.return_value = None
        super().test_endpoint_positive_contract()


# ---------------PATCH
class PatchEndpoint:
    url = None
    response_type = None
    status_code = None
    data_correct = {}
    data_422 = {
        "unreal_param": True
    }
    response = None
    mok = None

    def test_endpoint_positive_contract(self):
        response = client.patch(url=self.url, json=self.data_correct)
        # Сразу проверяем и статус, и структуру ответа
        assert response.status_code == self.status_code

    def test_param_is_not_exists(self):
        response = client.patch(url=self.url, json=self.data_422)
        assert response.status_code == 422


class TestEndPointAddItem(PatchEndpoint):
    url = "/basket/item/add"
    response_type = Basket
    status_code = 200
    data_correct = {
        "id_basket": "5",
        "id_item": "3",
        "count": 1
    }

    @pytest.mark.smoke
    @patch("blog.services.add_item_in_basket")
    def test_endpoint_positive_contract(self, mok_service):
        mok_service.return_value = Basket(id_basket="5", items=[BasketItem(id_item="3", count=1)])
        super().test_endpoint_positive_contract()


class TestEndpointChangeDescription(PatchEndpoint):
    url = "/item/change/description"
    response_type = ChangeItemDescriptionModel
    status_code = 204
    login = {"username": "manager_username", "password": "123", "admin": True}
    data_correct = {"data": {"id_item": "8387ef52-fc99-4321-bc3c-69d28047d00c", "new_description": "1232222"},
                    "credentials": login}

    @pytest.mark.smoke
    @patch("blog.services.change_item_description")
    def test_endpoint_positive_contract(self, mok_service):
        mok_service.return_value = None
        super().test_endpoint_positive_contract()


class TestEndpointChangePrice(PatchEndpoint):
    url = "/item/change/price"
    response_type = ChangeItemPriceModel
    status_code = 204
    login = {"username": "manager_username", "password": "123", "admin": True}
    data_correct = {"data": {"id_item": "8387ef52-fc99-4321-bc3c-69d28047d00c", "new_price": 1232222},
                    "credentials": login}

    @pytest.mark.smoke
    @patch("blog.services.change_item_price")
    def test_endpoint_positive_contract(self, mok_service):
        mok_service.return_value = None
        super().test_endpoint_positive_contract()
