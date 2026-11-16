
from pydantic import BaseModel, ConfigDict

from blog.domains import Basket, Manager


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # лишние поля — ошибка
        str_strip_whitespace=True,  # убрать пробелы
        validate_assignment=True,  # валидировать при изменении
    )


# --ITEMS--
class ItemWithoutID(StrictBaseModel):
    title: str
    description: str
    price: int


class Item(ItemWithoutID):
    id: str


class GetItemsModel(StrictBaseModel):
    items: list[Item]


class ParamsItemModel(StrictBaseModel):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None


class ChangeItemModel(StrictBaseModel):
    id: str
    title: str | None = None
    description: str | None = None
    price: int | None = None


# class CreateItemModel(StrictBaseModel):
#     title: str
#     description: str
#     price: int


# class ChangeItemDescriptionModel(StrictBaseModel):
#     item_id: str
#     new_description: str


# class ChangeItemPriceModel(StrictBaseModel):
#     item_id: str
#     new_price: int


# __BASKET__
class GetBasketsModel(StrictBaseModel):
    baskets: list[Basket]


class AddItemModel(StrictBaseModel):
    basket_id: str
    item_id: str
    count: int


class RepresentBasketModel(StrictBaseModel):
    basket_id: str
    items: list[BasketRepresentItem]


class BasketRepresentItem(StrictBaseModel):
    item_id: str
    count: int


class ItemBasketDeleteModel(StrictBaseModel):
    basket_id: str
    item_id: str


# __register__



class User(StrictBaseModel):
    email: str

class FullUser(User):
    id: str

class LoginModel(StrictBaseModel):
    username: str
    password: str


class ErrorModel(StrictBaseModel):
    detail: str


class NewManager(StrictBaseModel):
    user_id: str
    username: str
    password: str
    admin: bool


class GetUsersModel(StrictBaseModel):
    users: list[User | Manager]


class OrderModel(StrictBaseModel):
    email: str
    basket_id: str


class RegisterUserModel(StrictBaseModel):
    email: str


# ----------------FILTERS
class ParamsUserModel(StrictBaseModel):
    """Обычный пользователь"""
    id: str | None = None
    email: str | None = None


class ParamsBasketModel(StrictBaseModel):
    basket_id: str | None = None


class ParamsManagerModel(StrictBaseModel):
    user_id: str | None = None
    username: str | None = None
    is_admin: bool | None = None
