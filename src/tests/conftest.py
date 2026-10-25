import shelve

import pytest
from sqlalchemy.orm import sessionmaker

from blog.db import make_engine, make_session_factory
from blog.domains import User, Manager
from blog.models import Base, User as UserModel, Item as ItemModel, Manager as ManagerModel , Basket as BasketModel, BasketItem as BasketItemModel


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

@pytest.fixture
def postgres_db_test():
    DEFAULT_DSN = "postgresql+psycopg://postgres:toadbest@localhost:5432/shop_db_test"
    engine = make_engine(DEFAULT_DSN)
    Base.metadata.create_all(engine)  # создаем таблицы 1 раз

    # 1. Открываем соединение и "пленку" (транзакцию)
    connection = engine.connect()
    transaction = connection.begin()

    # 2. Создаем фабрику сессий, привязанную к ЭТОМУ соединению
    #    (важно: bind=connection, а не engine)
    SessionLocal = sessionmaker(bind=connection, expire_on_commit=False)

    yield SessionLocal  # отдаем тесту

    # 3. После теста — откатываем всё и закрываем
    transaction.rollback()
    connection.close()


@pytest.fixture
def seed_data_items(postgres_db_test):
    """
    Эта фикстура создает предсказуемые данные ДО начала теста.
    """
    # postgres_db_test — это фабрика сессий (sessionmaker), привязанная к транзакции
    with postgres_db_test() as session:

        # 2. Создаем товар с ФИКСИРОВАННЫМ id
        item = ItemModel(id="item_1", title="Test Item", description="Desc", price=100)
        session.add(item)
        item = ItemModel(id="item_2", title="Test Item", description="Desc2", price=1002)
        session.add(item)
        item = ItemModel(id="item_3", title="Test Item3", description="Desc2", price=1003)
        session.add(item)
        item = ItemModel(id="item_4", title="Test Item4", description="Desc4", price=100)
        session.add(item)



    # Возвращаем словарь с этими id, чтобы тест мог их использовать
    yield {
        "items_ids": ["item_1", "item_2", "item_3", "item_4"],
    }

@pytest.fixture
def seed_data_users(postgres_db_test):
    """
    Эта фикстура создает предсказуемые данные ДО начала теста.
    """
    # postgres_db_test — это фабрика сессий (sessionmaker), привязанная к транзакции
    with postgres_db_test() as session:
        # 1. Создаем пользователя с ФИКСИРОВАННЫМ id
        user = UserModel(id="user_1", email="test1@example.com")
        session.add(user)
        user = UserModel(id="user_2", email="test2@example.com")
        session.add(user)
        user = UserModel(id="user_3", email="test3@example.com")
        session.add(user)
        user = UserModel(id="user_4", email="test4@example.com")
        session.add(user)

        # session.commit()  # Коммитим в нашу "пленку" (транзакцию)

    # Возвращаем словарь с этими id, чтобы тест мог их использовать
    yield {
        "user_ids": "user_1",

    }


@pytest.fixture
def seed_data_managers(postgres_db_test, seed_data_users):
    """
    Эта фикстура создает предсказуемые данные ДО начала теста.
    """
    # postgres_db_test — это фабрика сессий (sessionmaker), привязанная к транзакции
    with postgres_db_test() as session:
        # 1. Создаем пользователя с ФИКСИРОВАННЫМ id
        manager = ManagerModel(user_id="user_1", username="username_1", password="password_1", is_admin=True)
        session.add(manager)
        manager = ManagerModel(user_id="user_2", username="username_2", password="password_2", is_admin=False)
        session.add(manager)
        manager = ManagerModel(user_id="user_3", username="username_1", password="password_1", is_admin=True)
        session.add(manager)



    # Возвращаем словарь с этими id, чтобы тест мог их использовать
    yield {
        "managers_ids": ["user_1", "user_2", "user_3", "user_4"],
    }

@pytest.fixture
def seed_data_basket(postgres_db_test,seed_data_basket, seed_data_items):
    """
    Эта фикстура создает предсказуемые данные ДО начала теста.
    """
    # postgres_db_test — это фабрика сессий (sessionmaker), привязанная к транзакции
    with postgres_db_test() as session:
        # 1. Создаем пользователя с ФИКСИРОВАННЫМ id
        basket = BasketModel(id="basket_1", items=[
            BasketItemModel(id="basket_item_1", basket_id="basket_1", item_id="item_1", count=1),
            BasketItemModel(id="basket_item_2", basket_id="basket_1", item_id="item_2", count=2),
        ])
        session.add(basket)
        basket = BasketModel(id="basket_2", items=[
            BasketItemModel(id="basket_item_1", basket_id="basket_1", item_id="item_1", count=1),
        ])
        session.add(basket)
        basket = BasketModel(id="basket_3", items=[])
        session.add(basket)



    # Возвращаем словарь с этими id, чтобы тест мог их использовать
    yield {
        "managers_ids": ["user_1", "user_2", "user_3", "user_4"],
    }

@pytest.fixture
def seed_data_basket_item(postgres_db_test,se):
    """
    Эта фикстура создает предсказуемые данные ДО начала теста.
    """
    with postgres_db_test() as session:

        bi = BasketItemModel(id="basket_item_1", basket_id="basket_1", item_it="item_1", count=1)
        session.add(bi)
        bi = BasketItemModel(id="basket_item_2", basket_id="basket_1", item_it="item_2", count=2)
        session.add(bi)



    # Возвращаем словарь с этими id, чтобы тест мог их использовать
    yield {
        "ids": ["basket_item_1", "basket_item_2"],
    }