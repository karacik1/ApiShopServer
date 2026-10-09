import shelve
from abc import ABC, abstractmethod
from blog.domains import Item, Manager, User, Basket


class ManagersRepository(ABC):
    """
        Абстрактный репозиторий для пользователей.
        От него нужно наследоваться в случае, когда нужно сделать другое хранилище, старое переписывать не нужно.
    """

    @abstractmethod
    def get_users(self, username: str | None, password: str | None, admin: bool | None) -> list[User]:
        pass


class ShelveManagersRepository(ManagersRepository):
    """
        Реализация пользовательского хранилища в оперативной памяти.
        Пользователи инициализируются во время инициализации репозитория
    """

    def __init__(self):
        self.db_name = "users.db"
        with shelve.open(self.db_name) as db:
            if "1" not in db:
                db["1"] = Manager(id="1", username="1", password="1", admin=True)

    def get_users(
        self,
        username: str | None = None,
        password: str | None = None,
        admin: bool | None = None,
    ) -> list[User]:
        with shelve.open(self.db_name) as db:
            users = list(db.values())
        result = []
        for user in users:
            if username is not None and user.username != username:
                continue
            if password is not None and user.password != password:
                continue
            if admin is not None and user.admin != admin:
                continue
            result.append(user)
        return result

    def create_user(self, user: User) -> User:
        with shelve.open(self.db_name) as db:
            db[user.id] = user
        return user


class ItemRepository(ABC):
    @abstractmethod
    def get_items(self) -> list[Item]:
        pass

    @abstractmethod
    def get_item(self, item_id: str) -> list[Item] | int:
        pass

    @abstractmethod
    def create_item(self, item: Item) -> None:
        pass

    @abstractmethod
    def change_item_description(self, item_id: str, new_description: str) -> None:
        pass

    @abstractmethod
    def change_item_price(self, item_id: str, new_price: int) -> None:
        pass


class ShelveItemsRepository(ItemRepository):
    def __init__(self):
        self.db_name = "items.db"

    def get_items(self) -> list[Item]:
        with shelve.open(self.db_name) as db:
            return list(db.values())

    def get_item(self, item_id: str) -> list[Item] | int:
        """
        если вещь не найдена возвращает -1
        если айди пишется в ключ, то можно будет проще сделать
        :param item_id:
        :param id:
        :return:
        """
        with shelve.open(self.db_name) as db:
            for item in list(db.values()):
                if item["id"] == item_id:
                    return item
            return -1

    def change_item_description(self, item_id: str, new_description: str) -> None:
        with shelve.open(self.db_name) as db:
            for key, item in list(db.items()):
                if item.id == item_id:
                    item.description = new_description
                    db[key] = item

    def change_item_price(self, item_id: str, new_price: int) -> None:
        with shelve.open(self.db_name) as db:
            for key, item in list(db.items()):
                if item.id == item_id:
                    item.price = new_price
                    db[key] = item

    def create_item(self, item: Item):

        with shelve.open(self.db_name) as db:
            db[item.id] = item


class BasketsRepository(ABC):

    @abstractmethod
    def get_baskets(self) -> list[Basket]:
        pass

    @abstractmethod
    def get_basket(self, id_user) -> list[Basket]:
        pass

    @abstractmethod
    def add_item(self, new_basket: Basket) -> list[Basket]:
        pass

    @abstractmethod
    def delete_item(self, id_user: str, id_item: str, ) -> None:
        pass

    @abstractmethod
    def delete_basket(self, id_user) -> None:
        pass


class ShelveBasketsRepository(BasketsRepository):
    def __init__(self):
        self.db_name = "baskets.db"

    def get_baskets(self) -> list[Basket]:
        with shelve.open(self.db_name) as db:
            return list(db.values())

    def get_basket(self, id_user) -> list[Basket]:
        current_items = []
        with shelve.open(self.db_name) as db:
            for basket in list(db.values()):
                if basket.id_user == id_user:
                    current_items.append(basket)
            return current_items

    def add_item(self, new_basket: Basket) -> list[Basket]:
        with shelve.open(self.db_name) as db:
            db[new_basket.id] = new_basket
            return db[new_basket.id]

    def delete_item(self, id_user: str, id_item: str, ) -> None:
        with shelve.open(self.db_name) as db:
            for basket in db.values():
                if basket.id_user == id_user and basket.id_item == id_item:
                    del db[basket.id]

    def delete_basket(self, id_user) -> None:
        with shelve.open(self.db_name) as db:
            for key, basket in db.items():
                if basket.id_user == id_user:
                    del db[key]
