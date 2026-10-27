import pytest
from sqlalchemy import select

from blog import services
from blog.models import User as UserModel, Manager as ManagerModel
from blog.repositories import PostgresUserRepository, PostgresManagerRepository
from blog.schemas import ParamsUserModel, NewManager
from blog.domains import User as UserDomain, Manager as ManagerDomain


class TestUserService:
    # REGISTER
    def test_create_new_user(self, postgres_db_test):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        data = "test_email"
        service.register(data)

        with postgres_db_test() as session:
            users = select(UserModel).where(UserModel.email == data)
            users = session.execute(users).scalars().all()
            assert len(users) == 1

    def test_create_users_with_exists_email(self, postgres_db_test):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        old_data = "test_email"
        service.register(old_data)

        data = "test_email"
        with pytest.raises(ValueError, match="Email test_email exists"):
            service.register(data)

    def test_login_user(self,postgres_db_test, seed_data_users):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        exists_data_email = "test1@example.com"
        result = service.login(email = exists_data_email)

        assert result == UserDomain(email="test1@example.com")

    # GET_USERS
    def test_get_user_by_id_email(self, postgres_db_test, seed_data_users):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        filter_by_email = ParamsUserModel(
            email="test4@example.com")

        filter_by_id = ParamsUserModel(
            id="user_1",)


        user_by_id = service.get_users(filters=filter_by_id)
        user_by_email = service.get_users(filters=filter_by_email)

        assert len(user_by_id) == 1
        assert len(user_by_email) == 1

class TestManagerService:
    def test_add_manager(self, postgres_db_test, seed_data_managers):
        repro = PostgresManagerRepository(postgres_db_test)
        service = services.ManagerService(repro)

        with postgres_db_test() as session:
            stmt = select(ManagerModel)
            old_manager_count = session.execute(stmt).scalars().all()

        new_manager = ManagerDomain(
            user_id="user_4",
            username="test_name",
            password="test_password",
            is_admin=True,
        )
        service.add_manager(new_manager)

        with postgres_db_test() as session:
            stmt = select(ManagerModel)
            new_manager_count = session.execute(stmt).scalars().all()

        assert len(new_manager_count) == 1+len(old_manager_count)

