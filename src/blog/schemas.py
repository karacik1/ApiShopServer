from multiprocessing import managers

from pydantic import BaseModel

from blog.domains import Basket, User, Manager, Item


# --ITEMS--
class GetItemModel(BaseModel):
    item_id: str
    title: str
    description: str
    price: int

class CreateItemModel(BaseModel):
    credentials: LoginModel
    title: str
    description: str
    price: int

class GetItemsModel(BaseModel):
    items: list[Item]

class ChangeItemDescriptionModel(BaseModel):
    credentials: LoginModel
    item_id: str
    new_description: str

class ChangeItemPriceModel(BaseModel):
    credentials: LoginModel
    item_id: str
    new_price: int

# __BASKET__
class GetBasketsModel(BaseModel):
    baskets: list[Basket]

class BasketModel(BaseModel):
    id_basket: str
    id_item: str
    count: int

class AddItemModel(BaseModel):
    id_basket: str
    id_item: str
    count: int


class ItemBasketDeleteModel(BaseModel):
    id_basket: str
    id_item: str

# __register__
class LoginModel(BaseModel):
    username: str
    password: str
    admin: bool

class ErrorModel(BaseModel):
    detail: str

class UserProfileModel(BaseModel):
    username: str
    email: str
    basket_UUID: str
    baskets: list[BasketModel]

class GetUsersModel(BaseModel):
    users: list[User | Manager]

class OrderModel(BaseModel):
    email: str
    id_basket: str

class ParamsUserModel(BaseModel):
    """Обычный пользователь"""
    id: str | None = None
    username: str | None = None
    email: str | None = None
    basket_UUID: str | None = None
    admin: bool | None = None

class ParamsItemModel(BaseModel):
    id: str | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None