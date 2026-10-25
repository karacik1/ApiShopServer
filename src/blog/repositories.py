from uuid import uuid4

from sqlalchemy import select

from blog.domains import Item as ItemDomain, Manager as ManegerDomain, User as UserDomain, BasketItem
from blog.models import User as UserModel, Item as ItemModel, Manager as ManagerModel, Basket as BasketModel
from blog.schemas import ParamsUserModel, ParamsItemModel, AddItemModel, ParamsManagerModel


# class Repository(ABC):
#     """
#         Абстрактный репозиторий для пользователей.
#         От него нужно наследоваться в случае, когда нужно сделать другое хранилище, старое переписывать не нужно.
#     """
#     @abstractmethod
#     def get(self, key: str) :
#         pass
#
#     @abstractmethod
#     def delete(self, key: str) -> None:
#         pass
#
#     @abstractmethod
#     def get_all(self, filters) :
#         pass
#
#     @abstractmethod
#     def save(self, key: str, obj: ManegerDomain | UserDomain | Basket | ItemDomain | BasketItem, overwrite: bool = False) -> None:
#         pass
#
# class ShelveRepository(Repository):
#     def __init__(self, db_name: str):
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#
#         # 2. Поднимаемся на 2 уровня вверх (до корня StepikCourseTest)
#         # (src/blog -> src -> StepikCourseTest)
#         project_root = os.path.dirname(os.path.dirname(current_dir))
#
#         # 3. Формируем путь к папке data
#         data_dir = os.path.join(project_root, "data")
#
#         # 4. Если папки data нет — создаем её
#         os.makedirs(data_dir, exist_ok=True)
#
#         # 5. Итоговый путь к файлу БД
#         self.db_name = os.path.join(data_dir, db_name)
#
#
#         # Если это база пользователей — проверяем админа
#         if self.db_name.endswith("users.db"):
#             if not self.get_all({"id": "uniq_admin_id"}):
#                 admin = ManegerDomain(
#                     id="uniq_admin_id",
#                     username="manager_username",
#                     is_admin=True,
#                     password="123",
#                 )
#
#                 self.save(key=admin.id, obj=admin, overwrite=True)
#
#
#     def get_all(self, filters: dict) -> list :
#         """получает список параметров и значений который должны быть для сортировки.
#         принимает только конкретные значения"""
#         data = []
#
#         with shelve.open(self.db_name) as db:
#             for item_indx, item in db.items():
#                 for param_key, param_value in filters.items():
#                     if not hasattr(item, param_key):
#                         break
#                     if getattr(item, param_key) != param_value:
#                         break
#                 else: data.append(db[item_indx])
#
#
#             return data
#
#     def get(self, key: str):
#         with shelve.open(self.db_name) as db:
#             return db.get(key)
#
#     def delete(self, key: str) :
#         with shelve.open(self.db_name) as db:
#             if str(key) not in db:
#                 raise ValueError(f"Key {key} does not exist")
#             del db[str(key)]
#
#     def save(self, key, obj: ManegerDomain | UserDomain | Basket | ItemDomain | BasketItem, overwrite=False):
#         with shelve.open(self.db_name) as db:
#             if overwrite:
#                 db[str(key)] = obj
#             else:
#                 if self.get(key) is not None:
#                     raise ValueError(f"Key {key} already exists. Use overwrite=True")
#                 else:
#                     db[str(key)] = obj
#
#
#     def __len__(self):
#         with shelve.open(self.db_name) as db:
#             return len(db)
#
#     def add_item(self, item_id: str, count: int = 1) -> None:
#         for bi in self.items:
#             if bi.item_id == item_id:
#                 bi.count += count
#                 return
#         self.items.append(BasketItem(item_id, count))
#
#     def delete_item(self, item_id: str) -> None:
#         self.items = [bi for bi in self.items if bi.id_item != item_id]


class PostgresUserRepository:
    def __init__(self,session_factory):

        self.SessionLocal = session_factory

    def create(self, obj: UserDomain) -> None:

        with self.SessionLocal() as session:
            stmt = select(UserModel).where(UserModel.email == obj.email)
            user = session.execute(stmt).scalar_one_or_none()
            if user is None:
                session.add(UserModel(id=str(uuid4()), email=obj.email))
                session.commit()
                return
            raise ValueError(f"Email {obj.email} exists")

    def update(self, obj: UserDomain) -> None:
        with self.SessionLocal() as session:


            user = session.get(UserModel, obj.id)
            if user is not None:
                user.email = obj.email
                session.commit()
                return
            raise ValueError(f"ID {obj.id} does not exist")

    def delete(self, key: str) -> None:
        with self.SessionLocal() as session:
            stmt = select(UserModel).where(UserModel.id == key)
            user = session.execute(stmt).scalar_one_or_none()
            if user is not None:
                session.delete(user)
                session.commit()
                return
            raise ValueError(f"Key {key} does not exist")

    def get_all(self, filters: ParamsUserModel) -> list[UserDomain] :
        stmt = select(UserModel)
        with self.SessionLocal() as session:
            if filters.id:
                stmt = stmt.where(UserModel.id == filters.id)
            if filters.email:
                stmt = stmt.where(UserModel.email == filters.email)
            users = session.execute(stmt).scalars().all()

            domain_users = []
            for user in users:
                domain_users.append(UserDomain(id=user.id, email=user.email))
            return domain_users

    def get(self, key) -> UserDomain :
        with self.SessionLocal() as session:

            stmt = select(UserModel).where(UserModel.id == key)
            user = session.execute(stmt).scalar_one_or_none()
            if user is not None:
                return UserDomain(id=user.id, email=user.email)
            raise ValueError(f"ID {key} does not exist")

class PostgresItemRepository:
    def __init__(self,session_factory):
        self.SessionLocal = session_factory

    def create(self, data: ItemDomain) -> None:
        with self.SessionLocal() as session:
            item = session.get(ItemModel, data.id)
            if item is not None:
                raise ValueError(f"Item {data.id} already exists")

            session.add(ItemModel(id=data.id, title=data.title,description=data.description, price=data.price))
            session.commit()

    def delete(self, key: str) -> None:
        with self.SessionLocal() as session:
            item = session.get(ItemModel, key)
            if item is None:
                raise ValueError(f"Item {key} does not exist")

            session.delete(item)
            session.commit()

    def update(self,data: ItemDomain) -> None:
        with self.SessionLocal() as session:
            item = session.get(ItemModel, data.id)
            if item is None:
                raise ValueError(f"Item {data.id} does not exist")
            item.title = data.title
            item.description = data.description
            item.price = data.price

            session.commit()

    def get_all(self, filters: ParamsItemModel) -> list[ItemDomain]:
        with self.SessionLocal() as session:
            stmt = select(ItemModel)
            if filters.id is not None:
                stmt= stmt.where(ItemModel.id == filters.id)

            if filters.title is not None:
                stmt= stmt.where(ItemModel.title == filters.title)

            if filters.description is not None:
                stmt= stmt.where(ItemModel.description == filters.description)

            if filters.price is not None:
                stmt= stmt.where(ItemModel.price == filters.price)

            items = session.execute(stmt).scalars().all()
            return [ItemDomain(item.id, item.title, item.description, item.price) for item in items]

    def get(self, key: str) -> ItemDomain:
        with self.SessionLocal() as session:
            item=session.get(ItemModel, key)
            if item is not None:
                return ItemDomain(item.id, item.title, item.description, item.price)
            raise KeyError(f"Item {key} does not exist")

class PostgresManagerRepository:
    def __init__(self,session_factory):
        self.SessionLocal = session_factory

    def update(self, data: ManegerDomain):
        with self.SessionLocal() as session:
            user = session.get(UserModel, data.user_id)
            if user is None:
                raise ValueError(f"User {data.user_id} does not exist")

            manager = session.get(ManagerModel, data.user_id)
            if manager is None:
                raise ValueError(f"Manager {data.user_id} does not exist")
            else:
                manager.username = data.username
                manager.password = data.password
                manager.is_admin = data.is_admin
                session.commit()

    def create(self, data: ManegerDomain):
        with self.SessionLocal() as session:
            user = session.get(UserModel, data.user_id)
            if user is None:
                raise ValueError(f"User {data.user_id} does not exist")

            manager = session.get(ManagerModel, data.user_id)
            if manager is None:
                session.add(ManagerModel(user_id=user.id, username=data.username, password=data.password, id_admin=data.is_admin))
                session.commit()
                return
            raise ValueError(f"Manager {data.user_id} already exists")

    def delete(self, key: str) -> None:
        """удаляет права администратора у пользователя, но оставляет как обычного пользователя"""

        with self.SessionLocal() as session:
            user = session.get(ManagerModel, key)
            if user is None:
                raise ValueError(f"Manager {key} does not exist")
            session.delete(user)
            session.commit()

    def get_all(self, filters: ParamsManagerModel) -> list[ManegerDomain]:
            with self.SessionLocal() as session:
                stmt = select(ManagerModel)
                if filters.user_id is not None:
                    stmt = stmt.where(ManagerModel.user_id == filters.user_id)

                if filters.username is not None:
                    stmt = stmt.where(ManagerModel.username == filters.username)

                if filters.is_admin is not None:
                    stmt = stmt.where(ManagerModel.is_admin == filters.is_admin)

                managers = session.execute(stmt).scalars().all()
                return [ManegerDomain(manager.id, manager.title, manager.description, manager.price) for manager in managers]

    # def get(self, key: str) -> ManagerDomain:
    #     with self.SessionLocal() as session:
    #         user = session.get(ManagerModel, key)
    #         if user is None:
    #             raise ValueError(f"Manager {key} does not exist")
    #         return ManagerDomain(id=user.i)
class PostgresBasketRepository:
    def __init__(self,session_factory):
        self.SessionLocal = session_factory

    def create(self)-> str:
        with self.SessionLocal() as session:
            key = str(uuid4())
            session.add(BasketModel(id=key))
            session.commit()
            return key

    def delete(self, key: str) -> None:
        with self.SessionLocal() as session:
            basket = session.get(BasketModel, key)
            if basket is None:
                raise ValueError(f"Basket {key} does not exist")
            session.delete(basket)
            session.commit()

    def delete_item(self, basket_id: str, item_id: str) -> None:
        with self.SessionLocal() as session:

            basket = session.get(BasketModel, basket_id)
            if basket is None:
                raise ValueError(f"Basket {basket_id} does not exist")

            stmt = select(BasketItem).where(BasketItem.basket_id == basket_id, BasketItem.item_id == item_id)
            item = session.execute(stmt).scalar_one_or_none()
            if item is None:
                raise ValueError(f"Item {item_id} does not exist")
            session.delete(item)
            session.commit()

    def add_item(self, data:AddItemModel ) -> None:
        with self.SessionLocal() as session:
            basket = session.get(BasketModel, data.basket_id)
            if basket is None:
                raise ValueError(f"Basket {data.basket_id} does not exist")

            stmt = select(BasketItem).where(BasketItem.basket_id == data.basket_id, BasketItem.item_id == data.item_id)
            item = session.execute(stmt).scalar_one_or_none()
            if item is not None:
                item.count += data.count
            else:
                session.add(BasketItem(id=str(uuid4()), basket_id=data.basket_id, item_id=data.item_id, count=data.count))
            session.commit()



