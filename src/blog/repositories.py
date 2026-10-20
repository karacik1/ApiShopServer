import os
import shelve
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from blog.domains import Item, Manager, User, Basket, BasketItem
from blog.schemas import NewManager


class Repository(ABC):
    """
        Абстрактный репозиторий для пользователей.
        От него нужно наследоваться в случае, когда нужно сделать другое хранилище, старое переписывать не нужно.
    """
    @abstractmethod
    def get(self, key: str) -> Manager | User | Basket | Item | BasketItem:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def get_all(self, filters) -> list[Manager | User | Basket | Item | BasketItem]:
        pass

    @abstractmethod
    def save(self, key: str, obj: Manager | User | Basket | Item, overwrite: bool = False) -> None:
        pass

class ShelveRepository(Repository):
    def __init__(self, db_name: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. Поднимаемся на 2 уровня вверх (до корня StepikCourseTest)
        # (src/blog -> src -> StepikCourseTest)
        project_root = os.path.dirname(os.path.dirname(current_dir))

        # 3. Формируем путь к папке data
        data_dir = os.path.join(project_root, "data")

        # 4. Если папки data нет — создаем её
        os.makedirs(data_dir, exist_ok=True)

        # 5. Итоговый путь к файлу БД
        self.db_name = os.path.join(data_dir, db_name)


        # Если это база пользователей — проверяем админа
        if self.db_name.endswith("users.db"):
            if not self.get_all({"id": "uniq_admin_id"}):
                admin = Manager(
                    id="uniq_admin_id",
                    email="manager_email",
                    username="manager_username",
                    admin=True,
                    password="123",
                )
                self.save(key=admin.id, obj=admin, overwrite=True)


    def get_all(self, filters: dict) -> list :
        """получает список параметров и значений который должны быть для сортировки.
        принимает только конкретные значения"""
        data = []

        with shelve.open(self.db_name) as db:
            for item_indx, item in db.items():
                for param_key, param_value in filters.items():
                    if not hasattr(item, param_key):
                        break
                    if getattr(item, param_key) != param_value:
                        break
                else: data.append(db[item_indx])


            return data

    def get(self, key: str):
        with shelve.open(self.db_name) as db:
            return db.get(key)

    def delete(self, key: str) :
        with shelve.open(self.db_name) as db:
            if str(key) not in db:
                raise ValueError(f"Key {key} does not exist")
            del db[str(key)]

    def save(self, key, obj: Manager | User | Basket | Item, overwrite=False):
        with shelve.open(self.db_name) as db:
            if overwrite:
                db[str(key)] = obj
            else:
                if self.get(key) is not None:
                    raise ValueError(f"Key {key} already exists. Use overwrite=True")
                else:
                    db[str(key)] = obj


    def __len__(self):
        with shelve.open(self.db_name) as db:
            return len(db)

    def add_item(self, id_item: str, count: int = 1) -> None:
        for bi in self.items:
            if bi.id_item == id_item:
                bi.count += count
                return
        self.items.append(BasketItem(id_item, count))

    def delete_item(self, id_item: str) -> None:
        self.items = [bi for bi in self.items if bi.id_item != id_item]


