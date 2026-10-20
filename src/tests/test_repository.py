# --------------REPOSITORY METHODS
import shelve

import pytest

from blog.domains import User
from blog.repositories import ShelveRepository


class TestShelveGetAll:
    @pytest.mark.unit
    def test_get_users_by_email(self, user_db_test):
        filters = {"email": "email2"}
        repro = ShelveRepository(db_name=user_db_test)
        users = repro.get_all(filters=filters)
        assert len(users) == 1

    @pytest.mark.unit
    def test_get_admins(self, user_db_test):
        filters = {"is_admin": True}
        repro = ShelveRepository(db_name=user_db_test)
        users = repro.get_all(filters=filters)
        assert len(users) == 2

    @pytest.mark.unit
    def test_filter_by_nonexistent_value(self, user_db_test):
        repro = ShelveRepository(db_name=user_db_test)
        users = repro.get_all({"email": "нет-такого"})
        assert users == []

    @pytest.mark.unit
    def test_get_all_users(self, user_db_test):
        filters = {}
        repro = ShelveRepository(db_name=user_db_test)
        users = repro.get_all(filters=filters)
        assert len(users) == 5

# ----------------------------SHELVEMETHODS
class TestShelveSave:

    @pytest.mark.unit
    def test_shelve_add_new_row(self, user_db_test):
        repro = ShelveRepository(db_name=user_db_test)
        count = len(repro)
        repro.save(key="5", obj=User(id="5", email=""))
        assert len(repro) == count + 1

    @pytest.mark.unit
    def test_save_stores_correct_object(self, user_db_test):
        """Save записывает именно тот объект, что передан."""
        repro = ShelveRepository(db_name=user_db_test)
        obj = User(id="5", email="")

        repro.save(key="5", obj=obj)

        with shelve.open(user_db_test) as db:
            assert "5" in db
            assert db["5"] == obj

    @pytest.mark.unit
    def test_shelve_dont_add_new_row(self, user_db_test):
        repro = ShelveRepository(db_name=user_db_test)
        count = len(repro)
        obj = User(id="3", email="new_overwrited_email")
        repro.save(key="3", obj=obj, overwrite=True)

        assert len(repro) == count

    @pytest.mark.unit
    def test_save_overwrite_data(self, user_db_test):
        repro = ShelveRepository(db_name=user_db_test)
        obj = User(id="3", email="new_overwrited_email")
        repro.save(key="3", obj=obj, overwrite=True)

        with shelve.open(user_db_test) as db:
            assert "3" in db
            assert db["3"] == obj

    # -------------------------------------error
    @pytest.mark.unit
    def test_save_data_with_old_key(self, user_db_test):
        with pytest.raises(ValueError, match="Key 3 already exists. Use overwrite=True"):
            repro = ShelveRepository(db_name=user_db_test)
            obj = User(id="3", email="new_overwrited_email")
            repro.save(key="3", obj=obj)


class TestShelveDelete:
    @pytest.mark.unit
    def test_shelve_delete(self, user_db_test):
        repro = ShelveRepository(db_name=user_db_test)
        count = len(repro)
        repro.delete(key="3")
        assert len(repro) == count - 1

    # -------------------------------------error
    @pytest.mark.unit
    def test_shelve_key_not_exists(self, user_db_test):
        with pytest.raises(ValueError, match="Key 5 does not exist"):
            repro = ShelveRepository(db_name=user_db_test)
            repro.delete(key="5")
