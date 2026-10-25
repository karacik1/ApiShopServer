import pytest
from sqlalchemy import select

from blog import services
from blog.models import User as UserModel
from blog.repositories import PostgresUserRepository



class TestUserService:
    # REGISTER
    def test_create_new_user(self, postgres_db_test):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        data = "test_email"
        service.register(data)

        with postgres_db_test() as session:
            users = select(UserModel).where(UserModel.email == data)
            users = session.execute(users).scalaers().all()
            assert len(users) == 1

    def test_create_users_with_exists_email(self, postgres_db_test):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)
        old_data = "test_email"
        service.register(old_data)

        data = "test_email"
        with pytest.raises(ValueError, match="Email test_email exists"):
            service.register(data)

    #GET_USERS





