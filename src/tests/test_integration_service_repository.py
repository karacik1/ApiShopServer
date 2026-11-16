import pytest
from sqlalchemy import select

from blog import services
from blog.domains import User as UserDomain, Manager as ManagerDomain, Basket as BasketDomain, BasketItem as BasketItemDomain
from blog.models import User as UserModel, Manager as ManagerModel, Item as ItemModel, Basket as BasketModel, \
    BasketItem as BasketItemModel
from blog.repositories import PostgresUserRepository, PostgresManagerRepository, PostgresItemRepository, \
    PostgresBasketRepository
from blog.schemas import ParamsUserModel, ParamsItemModel, ChangeItemModel, ItemBasketDeleteModel, Item as ItemDomain
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


class TestItemService:
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
            title="NEW_TEST_TITLE",
            description="NEW_TEST_DESCRIPTION",
            price=1000000,
        )

        service.change_item_param(data=data)

        changed_item = service.get_items(filters=ParamsItemModel(id=data.id))

        assert changed_item[0].description == data.description
        assert changed_item[0].title == data.title
        assert changed_item[0].price == data.price


class TestBasketService:
    def test_create_basket(self, postgres_db_test, seed_data_basket):
        repro = PostgresBasketRepository(postgres_db_test)
        service = services.BasketService(repro)

        with postgres_db_test() as session:
            stmt = select(BasketModel)
            old_basket_count = session.execute(stmt).scalars().all()

        service.create_basket()

        with postgres_db_test() as session:
            stmt = select(BasketModel)
            new_basket_count = session.execute(stmt).scalars().all()

        assert len(new_basket_count) == 1 + len(old_basket_count)

    def test_delete_basket(self, postgres_db_test, seed_data_basket):
        repro = PostgresBasketRepository(postgres_db_test)
        service = services.BasketService(repro)

        with postgres_db_test() as session:
            stmt = select(BasketModel)
            old_basket_count = session.execute(stmt).scalars().all()

        basket_for_delete = "basket_1"
        service.delete_basket(basket_id=basket_for_delete)

        with postgres_db_test() as session:
            stmt = select(BasketModel)
            new_basket_count = session.execute(stmt).scalars().all()

        assert len(new_basket_count) == len(old_basket_count) - 1

    def test_add_item_in_basket(self, postgres_db_test, seed_data_basket):
        repro = PostgresBasketRepository(postgres_db_test)
        service = services.BasketService(repro)
        item_id = "item_3"
        basket_id = "basket_1"
        count = 1

        with postgres_db_test() as session:
            stmt = select(BasketItemModel).where(
                BasketItemModel.item_id == item_id,
                BasketItemModel.basket_id == basket_id,
                BasketItemModel.count == count)
            old_basket_count = session.execute(stmt).scalar_one_or_none()

        service.add_item_in_basket(item_id=item_id, basket_id=basket_id, count=count)

        with postgres_db_test() as session:
            stmt = select(BasketItemModel).where(
                BasketItemModel.item_id == item_id,
                BasketItemModel.basket_id == basket_id,
                BasketItemModel.count == count)
            new_basket_count = session.execute(stmt).scalar_one_or_none()

        assert old_basket_count is None
        assert new_basket_count is not None

    def test_delete_item_in_basket(self, postgres_db_test, seed_data_basket):
        repro = PostgresBasketRepository(postgres_db_test)
        service = services.BasketService(repro)
        item_id = "item_1"
        basket_id = "basket_1"

        with postgres_db_test() as session:
            stmt = select(BasketItemModel).where(
                BasketItemModel.item_id == item_id,
                BasketItemModel.basket_id == basket_id)
            old_basket_count = session.execute(stmt).scalar_one_or_none()

        service.delete_item(ItemBasketDeleteModel(item_id=item_id, basket_id=basket_id))

        with postgres_db_test() as session:
            stmt = select(BasketItemModel).where(
                BasketItemModel.item_id == item_id,
                BasketItemModel.basket_id == basket_id)
            new_basket_count = session.execute(stmt).scalar_one_or_none()

        assert old_basket_count is not None
        assert new_basket_count is None

    def test_get_basket(self, postgres_db_test, seed_data_basket):
        repro = PostgresBasketRepository(postgres_db_test)
        service = services.BasketService(repro)

        basket = service.get_basket(basket_id="basket_1")
        print(basket)
        print("done")
        correct_result = BasketDomain(id="basket_1", items=[
            BasketItemDomain(id="basket_item_1", basket_id="basket_1", item_id="item_1", count=1),
            BasketItemDomain(id="basket_item_2", basket_id="basket_1", item_id="item_2", count=2)])
        assert basket == correct_result
