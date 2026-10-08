from pydantic import BaseModel

from blog.domains import Basket


# --ITEMS--
class GetItemModel(BaseModel):
    item_id: str
    title: str
    description: str
    price: int

class CreateItemModel(BaseModel):
    title: str
    description: str
    price: int

class GetItemsModel(BaseModel):
    items: list[GetItemModel]

class ChangeItemDescriptionModel(BaseModel):
    item_id: str
    new_description: str

class ChangeItemPriceModel(BaseModel):
    item_id: str
    new_price: int

# __BASKET__
class GetBasketsModel(BaseModel):
    basket: list[BasketModel]

class BasketModel(BaseModel):
    id_basket: str
    id_user: str
    id_item: str
    count: int

class SaveItemModel(BaseModel):
    id_basket: str
    id_user: str
    id_item: str
    count: int

# __register__
class LoginModel(BaseModel):
    username: str
    password: str

class LoginUserModel(BaseModel):
    email: str

class ErrorModel(BaseModel):
    detail: str




# я устала переписывать но вот валидация входа
# # --ITEMS--
# class GetItemModel(BaseModel):
#     item_id: int
#
# class CreateItemModel(BaseModel):
#     title: str
#     description: str
#     price: int
#
# class ChangeItemDescriptionModel(BaseModel):
#     item_id: str
#     new_description: str
#
# class ChangeItemPriceModel(BaseModel):
#     item_id: str
#     new_price: int
#
# # __BASKET__
# class GetBasketModel(BaseModel):
#     id_basket: str
#
# class AddItemInBasketModel(BaseModel):
#     id_basket: str
#     id_user: int
#     id_item: int
#     count: int
#
# class DeleteItemFromBasketModel(BaseModel):
#     id_basket: str
#     id_item: int
#
# class DeleteBasketModel(BaseModel):
#     id_basket: str
#
#
# # __register__
# class LoginModel(BaseModel):
#     username: str
#     password: str
#
# class LoginUserModel(BaseModel):
#     email: str
#
# class ErrorModel(BaseModel):
#     detail: str
