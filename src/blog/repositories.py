import shelve
from abc import ABC, abstractmethod
from blog.domains import Item, Manager, User, Basket


class UserRepository(ABC):
    """
        Абстрактный репозиторий для пользователей.
        От него нужно наследоваться в случае, когда нужно сделать другое хранилище, старое переписывать не нужно.
    """
    @abstractmethod
    def get_users(self, username: str | None, password: str | None) -> list[User]:
        pass


class ShelveUsersRepository(UserRepository):
    """
        Реализация пользовательского хранилища в оперативной памяти.
        Пользователи инициализируются во время инициализации репозитория
    """
    def __init__(self):
        self.users = [
            Manager(id="29ae7ebf-4445-42f2-9548-a3a54f095220",
                  username="admin",
                  password="Dimon4321!",
                    admin=True
            )
        ]
    def get_users(self, username: str | None, password: str | None) -> list[User]:
        """

        :param username: фильтр по логину
        :param password: фильтр по паролю
        :return: отфильтрованные пользователи
        """
        filtered_users = []
        for user in self.users:
            if username != username and username is not None:
                continue
            if password != password and password is not None:
                continue
            filtered_users.append(user)

class ItemRepository(ABC):
    @abstractmethod
    def get_items(self) -> list[Item]:
        pass

    @abstractmethod
    def get_item(self, item_id: int) -> list[Item] | int:
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
        self.db_name = "items"

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
    def delete_item(self, id_user: str, id_item: str,) -> None:
        pass

    @abstractmethod
    def delete_basket(self, id_user) -> None:
        pass

class ShelveBasketsRepository(BasketsRepository):
    def __init__(self):
        self.db_name = "baskets"

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

    def delete_item(self,id_user: str, id_item: str,) -> None:
        with shelve.open(self.db_name) as db:
            for basket in db.values():
                if basket.id_user == id_user and basket.id_item == id_item:
                    del db[basket.id]

    def delete_basket(self, id_user) -> None:
        with shelve.open(self.db_name) as db:
            for key,basket in db.items():
                if basket.id_user == id_user:
                    del db[key]