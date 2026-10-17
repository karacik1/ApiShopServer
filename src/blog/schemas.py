from multiprocessing import managers

from pydantic import BaseModel, ConfigDict

from blog.domains import Basket, User, Manager, Item

class StrictBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",           # лишние поля — ошибка
        str_strip_whitespace=True,  # убрать пробелы
        validate_assignment=True,   # валидировать при изменении
    )
# --ITEMS--



class GetItemModel(StrictBaseModel):
    item_id: str
    title: str
    description: str
    price: int

class CreateItemModel(StrictBaseModel):
    title: str
    description: str
    price: int

class GetItemsModel(StrictBaseModel):
    items: list[Item]

class ChangeItemDescriptionModel(StrictBaseModel):
    id_item: str
    new_description: str

class ChangeItemPriceModel(StrictBaseModel):
    id_item: str
    new_price: int

# __BASKET__
class GetBasketsModel(StrictBaseModel):
    baskets: list[Basket]

class BasketModel(StrictBaseModel):
    id_basket: str
    id_item: str
    count: int

class AddItemModel(StrictBaseModel):
    id_basket: str
    id_item: str
    count: int


class ItemBasketDeleteModel(StrictBaseModel):
    id_basket: str
    id_item: str

# __register__
class LoginModel(StrictBaseModel):
    username: str
    password: str
    admin: bool

class ErrorModel(StrictBaseModel):
    detail: str

class NewManager(StrictBaseModel):
    email: str
    username: str
    password: str
    admin: bool

class GetUsersModel(StrictBaseModel):
    users: list[User | Manager]

class OrderModel(StrictBaseModel):
    email: str
    id_basket: str



# ----------------FILTERS
class ParamsUserModel(StrictBaseModel):
    """Обычный пользователь"""
    id: str | None = None
    username: str | None = None
    email: str | None = None
    basket_UUID: str | None = None
    admin: bool | None = None

class ParamsItemModel(StrictBaseModel):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None

class ParamsBasketModel(StrictBaseModel):
    id_basket: str | None = None
