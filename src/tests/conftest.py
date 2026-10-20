import shelve

import pytest

from blog.domains import User, Manager


@pytest.fixture
def user_db_test(tmp_path):
    db_path = tmp_path / "users.db"

    with shelve.open(str(db_path)) as db:
        db["1"] = Manager(id="1",
                          username="Sam",
                          password="Sam",
                          is_admin=False)
        db["2"] = Manager(id="2",
                          username="Sam",
                          password="Sam",
                          is_admin=True)
        db["3"] = User(id="3",
                       email="email3",)
        db["4"] = User(id="4",
                       email="email2",)
        db["0"] = Manager(
                    id="uniq_admin_id",
                    username="manager_username",
                    is_admin=True,
                    password="123",
                )
    yield str(db_path)