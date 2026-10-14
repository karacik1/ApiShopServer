import shelve

import pytest

from blog.domains import User, Manager


@pytest.fixture
def test_user_db(tmp_path):
    db_path = tmp_path / "users.db"

    with shelve.open(str(db_path)) as db:
        db["1"] = Manager(id="1",
                          email="email1",
                          username="Sam",
                          password="Sam",
                          admin=False)
        db["2"] = Manager(id="2",
                          email="email2",
                          username="Sam",
                          password="Sam",
                          admin=True)
        db["3"] = User(id="3",
                       email="email3",)
        db["4"] = User(id="4",
                       email="email2",)
    yield str(db_path)