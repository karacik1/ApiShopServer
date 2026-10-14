import shelve

import pytest
from fastapi.testclient import TestClient
from blog.main import app
from blog.repositories import ShelveRepository

client = TestClient(app)
class TestGetUsers:
    def test_status_200(self):
        response = client.get("/users")
        assert response.status_code == 200

    def test_users_returns_list(self):
        response = client.get("/users").json()
        assert isinstance(response, dict)

class TestGetBaskets:
    def test_status_200(self):
        response = client.get("/baskets")
        assert response.status_code == 200

    def test_users_returns_list(self):
        response = client.get("/baskets").json()
        assert isinstance(response, dict)


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
        filters={}
        repro = ShelveRepository(db_name=test_user_db)
        users = repro.get_all(filters=filters)
        assert len(users) == 4

class TestShelveSave:
    def test_shelve_add_new_row(self, test_user_db):
        repro = ShelveRepository(db_name=test_user_db)
        count = len(repro)
        repro.save(key="5", obj = {"id": "5","email": ""})
        assert len(repro) == count+1

    def test_save_stores_correct_object(self, test_user_db):
        """Save записывает именно тот объект, что передан."""
        repro = ShelveRepository(db_name=test_user_db)
        obj = {"id": "5","email": ""}

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


