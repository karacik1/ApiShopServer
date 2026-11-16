import pytest
from sqlalchemy import select

from blog import services
from blog.domains import User as UserDomain, Manager as ManagerDomain, Item as ItemDomain
from blog.models import User as UserModel, Manager as ManagerModel, Item as ItemModel
from blog.repositories import PostgresUserRepository, PostgresManagerRepository, PostgresItemRepository
from blog.schemas import ParamsUserModel, ParamsItemModel, ChangeItemModel
from tests.conftest import postgres_db_test


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

    def test_login_user(self, postgres_db_test, seed_data_users):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        exists_data_email = "test1@example.com"
        result = service.login(email=exists_data_email)

        assert result == UserDomain(email="test1@example.com")

    # GET_USERS
    def test_get_user_by_id_email(self, postgres_db_test, seed_data_users):
        repro = PostgresUserRepository(postgres_db_test)
        service = services.UserService(repro)

        filter_by_email = ParamsUserModel(
            email="test4@example.com")

        filter_by_id = ParamsUserModel(
            id="user_1", )

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

        assert len(new_manager_count) == 1 + len(old_manager_count)


class TestItemsService:
    def test_create_item(self, postgres_db_test, seed_data_items):
        repro = PostgresItemRepository(postgres_db_test)
        service = services.ItemService(repro)

        with postgres_db_test() as session:
            stmt = select(ItemModel)
            old_item_count = session.execute(stmt).scalars().all()

        new_item = ItemDomain(
            title="new_item_test_title",
            description="new_item_test_description",
            price=100
        )
        service.create_item(data=new_item)

        with postgres_db_test() as session:
            stmt = select(ItemModel)
            new_item_count = session.execute(stmt).scalars().all()

        assert len(new_item_count) == 1 + len(old_item_count)

    def test_delete_item(self, postgres_db_test, seed_data_items):
        repro = PostgresItemRepository(postgres_db_test)
        service = services.ItemService(repro)

        with postgres_db_test() as session:
            stmt = select(ItemModel)
            old_item_count = session.execute(stmt).scalars().all()

        item_for_delete = "item_1"
        service.delete(key=item_for_delete)

        with postgres_db_test() as session:
            stmt = select(ItemModel)
            new_item_count = session.execute(stmt).scalars().all()

        assert len(new_item_count) == len(old_item_count) - 1

    def test_get_items(self, postgres_db_test, seed_data_items):
        repro = PostgresItemRepository(postgres_db_test)
        service = services.ItemService(repro)

        filter = ParamsItemModel(id=None,
                                 title=None,
                                 description=None,
                                 price=None)

        items = service.get_items(filters=filter)

        exists_items = [ItemModel(id="item_1", title="Test Item", description="Desc", price=100),
                        ItemModel(id="item_2", title="Test Item", description="Desc2", price=1002),
                        ItemModel(id="item_3", title="Test Item3", description="Desc2", price=1003),
                        ItemModel(id="item_4", title="Test Item4", description="Desc4", price=100), ]

        assert items == exists_items

    def test_change_item_params(self, postgres_db_test, seed_data_items):
        repro = PostgresItemRepository(postgres_db_test)
        service = services.ItemService(repro)

        data = ChangeItemModel(
            id="item_1",
            title= "NEW_TEST_TITLE",
            description="NEW_TEST_DESCRIPTION",
            price=1000000,
        )

        service.change_item_param(data=data)

        changed_item = service.get_items(filters=ParamsItemModel(id=data.id))

        assert changed_item[0].description == data.description
        assert changed_item[0].title == data.title
        assert changed_item[0].price == data.price
