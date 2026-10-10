from pydantic import BaseModel

from blog.domains import Basket, User


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
    items: list[GetItemModel]

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

class CreateBasketModel(BaseModel):
    basket_id: str


class ItemBasketDeleteModel(BaseModel):
    id_basket: str
    id_item: str

# __register__
class LoginModel(BaseModel):
    username: str
    password: str
    admin: bool

class LoginUserModel(BaseModel):
    email: str

class ErrorModel(BaseModel):
    detail: str

class UserProfileModel(BaseModel):
    username: str
    email: str
    basket_UUID: str
    baskets: list[BasketModel]

class GetUsersModel(BaseModel):
    users: list[User]

class OrderModel(BaseModel):
    email: str
    id_basket: str