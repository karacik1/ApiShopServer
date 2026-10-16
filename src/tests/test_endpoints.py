import shelve
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from blog.domains import Basket, BasketItem
from blog.main import app
from blog.repositories import ShelveRepository
from blog.schemas import GetItemsModel, ChangeItemDescriptionModel, ChangeItemPriceModel, LoginModel

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


class TestEndPointAddItem(PostEndpoint):
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
        mok_service.return_value = Basket(id_basket="5", items = [BasketItem(id_item="3", count=1)])
        super().test_endpoint_positive_contract()



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


class TestEndpointChangeDescription(PostEndpoint):
    url = "/item/change/description"
    response_type = ChangeItemDescriptionModel
    status_code = 201
    data_correct = {"credentials": {
        "username": "username",
        "password": "password",
        "admin": True
    },
        "item_id": "5",
        "new_description": "new_description"}

    @pytest.mark.smoke
    @patch("blog.services.change_item_description")
    def test_endpoint_positive_contract(self, mok_service):
        mok_service.return_value = None
        super().test_endpoint_positive_contract()


class TestEndpointChangePrice(PostEndpoint):
    url = "/item/change/price"
    response_type = ChangeItemPriceModel
    status_code = 201
    data_correct = {"credentials": {
        "username": "username",
        "password": "password",
        "admin": True
    },
        "item_id": "5",
        "new_price": 12}

    @pytest.mark.smoke
    @patch("blog.services.change_item_price")
    def test_endpoint_positive_contract(self, mok_service):

        mok_service.return_value = None
        super().test_endpoint_positive_contract()

#----------------DELETE
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
    status_code = 200
    data_correct = {
        "id_basket": "5",
    }

    @patch("blog.services.delete_basket")
    def test_endpoint_positive_contract(self, mok):
        mok.return_value = None
        super().test_endpoint_positive_contract()


class TestEndPointDeleteBasketItem(DeleteEndpoint):
    url = "/basket/item/delete"
    status_code = 200
    data_correct = {
        "id_basket": "5",
        "id_item": "1"
    }

    @patch("blog.services.delete_item")
    def test_endpoint_positive_contract(self, mok):
        mok.return_value = None
        super().test_endpoint_positive_contract()

# --------------REPOSITORY METHODS
class TestShelveGetAll:
    def test_get_users_by_email(self, test_user_db):
        filters = {"email": "email2"}
        repro = ShelveRepository(db_name=test_user_db)
        users = repro.get_all(filters=filters)
        assert len(users) == 2

    def test_get_admins(self, test_user_db):
        filters = {"admin": True}
        repro = ShelveRepository(db_name=test_user_db)
        users = repro.get_all(filters=filters)
        assert len(users) == 1

    def test_filter_by_nonexistent_value(self, test_user_db):
        repro = ShelveRepository(db_name=test_user_db)
        users = repro.get_all({"email": "нет-такого"})
        assert users == []

    def test_get_all_users(self, test_user_db):
        filters = {}
        repro = ShelveRepository(db_name=test_user_db)
        users = repro.get_all(filters=filters)
        assert len(users) == 4


class TestShelveSave:
    def test_shelve_add_new_row(self, test_user_db):
        repro = ShelveRepository(db_name=test_user_db)
        count = len(repro)
        repro.save(key="5", obj={"id": "5", "email": ""})
        assert len(repro) == count + 1

    def test_save_stores_correct_object(self, test_user_db):
        """Save записывает именно тот объект, что передан."""
        repro = ShelveRepository(db_name=test_user_db)
        obj = {"id": "5", "email": ""}

        repro.save(key="5", obj=obj)

        with shelve.open(test_user_db) as db:
            assert "5" in db
            assert db["5"] == obj

    def test_shelve_dont_add_new_row(self, test_user_db):
        repro = ShelveRepository(db_name=test_user_db)
        count = len(repro)
        obj = {"id": "3", "email": "new_overwrited_email"}
        repro.save(key="3", obj=obj, overwrite=True)

        assert len(repro) == count

    def test_save_overwrite_data(self, test_user_db):
        repro = ShelveRepository(db_name=test_user_db)
        obj = {"id": "3", "email": "new_overwrited_email"}
        repro.save(key="3", obj=obj, overwrite=True)

        with shelve.open(test_user_db) as db:
            assert "3" in db
            assert db["3"] == obj

    # -------------------------------------error

    def test_save_data_with_old_key(self, test_user_db):
        with pytest.raises(ValueError, match="Key 3 already exists. Use overwrite=True"):
            repro = ShelveRepository(db_name=test_user_db)
            obj = {"id": "3", "email": "new_overwrited_email"}
            repro.save(key="3", obj=obj)


class TestShelveDelete:
    def test_shelve_delete(self, test_user_db):
        repro = ShelveRepository(db_name=test_user_db)
        count = len(repro)
        repro.delete(key="3")
        assert len(repro) == count - 1

    # -------------------------------------error
    def test_shelve_key_not_exists(self, test_user_db):
        with pytest.raises(ValueError, match="Key 5 does not exist"):
            repro = ShelveRepository(db_name=test_user_db)
            repro.delete(key="5")
