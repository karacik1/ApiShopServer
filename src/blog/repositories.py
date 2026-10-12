import shelve
import uuid
from abc import ABC, abstractmethod
from blog.domains import Item, Manager, User, Basket, BasketItem

class Repository(ABC):
    """
        Абстрактный репозиторий для пользователей.
        От него нужно наследоваться в случае, когда нужно сделать другое хранилище, старое переписывать не нужно.
    """
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def save(self, key: str, obj) -> None:
        pass

class ShelveRepository(Repository):
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_all(self) :
        with shelve.open(self.db_name) as db:
            return list(db.values())

    def get(self, key: str):
        with shelve.open(self.db_name) as db:
            return db.get(key)

    def delete(self, key: str) :
        with shelve.open(self.db_name) as db:
            del db[str(key)]

    def save(self, key, obj):
        with shelve.open(self.db_name) as db:
            db[key] = obj

# class ShelveUserRepository(ShelveRepository):
#
#
# class ItemRepository(ABC):
#     @abstractmethod
#     def get_items(self) -> list[Item]:
#         pass
#
#     @abstractmethod
#     def get_item(self, item_id: str) -> list[Item] | int:
#         pass
#
#     @abstractmethod
#     def create_item(self, item: Item) -> None:
#         pass
#
#     @abstractmethod
#     def change_item_description(self, item_id: str, new_description: str) -> None:
#         pass
#
#     @abstractmethod
#     def change_item_price(self, item_id: str, new_price: int) -> None:
#         pass
#
#
# class ShelveItemsRepository(ItemRepository):
#     def __init__(self):
#         self.db_name = "items.db"
#
#     def get_items(self) -> list[Item]:
#         with shelve.open(self.db_name) as db:
#             return list(db.values())
#
#     def get_item(self, item_id: str) -> list[Item] | int:
#         """
#         если вещь не найдена возвращает -1
#         если айди пишется в ключ, то можно будет проще сделать
#         :param item_id:
#         :param id:
#         :return:
#         """
#         with shelve.open(self.db_name) as db:
#             for item in list(db.values()):
#                 if item["id"] == item_id:
#                     return item
#             return -1
#
#     def change_item_description(self, item_id: str, new_description: str) -> None:
#         with shelve.open(self.db_name) as db:
#             for key, item in list(db.items()):
#                 if item.id == item_id:
#                     item.description = new_description
#                     db[key] = item
#
#     def change_item_price(self, item_id: str, new_price: int) -> None:
#         with shelve.open(self.db_name) as db:
#             for key, item in list(db.items()):
#                 if item.id == item_id:
#                     item.price = new_price
#                     db[key] = item
#
#     def create_item(self, item: Item):
#
#         with shelve.open(self.db_name) as db:
#             db[item.id] = item
#
#
# class BasketsRepository(ABC):
#
#     @abstractmethod
#     def get_baskets(self) -> list[Basket]:
#         pass
#
#     @abstractmethod
#     def get_basket(self, id_basket) -> Basket | None:
#         pass
#
#     @abstractmethod
#     def add_item(self, id_basket: str, new_item: BasketItem) -> Basket:
#         pass
#
#     @abstractmethod
#     def delete_item(self, id_basket: str, id_item: str, ) -> None:
#         pass
#
#     @abstractmethod
#     def delete_basket(self, id_basket) -> None:
#         pass
#
#     @abstractmethod
#     def create_basket(self) -> str:
#         pass
#
#
# class ShelveBasketsRepository(BasketsRepository):
#     def __init__(self):
#         self.db_name = "baskets.db"
#
#     def create_basket(self) -> str:
#         with  shelve.open(self.db_name) as db:
#             id_basket = str(uuid.uuid4())
#             db[id_basket] = Basket(id_basket=id_basket, items=[])
#         return id_basket
#
#     def get_baskets(self) -> list[Basket]:
#         with shelve.open(self.db_name) as db:
#             return list(db.values())
#
#     def get_basket(self, id_basket) -> Basket | None:
#         with shelve.open(self.db_name) as db:
#             return db.get(id_basket)
#
#     def add_item(self, id_basket: str, new_item: BasketItem) -> Basket:
#         with shelve.open(self.db_name) as db:
#             basket = db.get(id_basket)
#             items = basket.items
#             for indx, item in enumerate(items):
#                 if new_item.id_item == item.id_item:
#                     item.count += new_item.count
#                     break
#             else:
#                 items.append(new_item)
#             db[id_basket] = basket
#         return basket
#
#     def delete_item(self, id_basket: str, id_item: str, ) -> None:
#         with shelve.open(self.db_name) as db:
#             basket = self.get_basket(id_basket)
#             for indx, item in enumerate(basket.items):
#                 if item.id_item == id_item:
#                     del basket.items[indx]
#                     break
#             db[id_basket] = basket
#
#     def delete_basket(self, id_basket) -> None:
#         with shelve.open(self.db_name) as db:
#             for key, basket in db.items():
#                 if basket.id_basket == id_basket:
#                     del db[key]

