from fastapi import APIRouter, status, HTTPException

from fastapi import APIRouter, status, HTTPException

from blog import services
from blog.domains import Basket, User
from blog.schemas import (
    GetItemModel,
    GetItemsModel,
    LoginModel,
    ErrorModel, CreateItemModel, ChangeItemDescriptionModel, ChangeItemPriceModel, AddItemModel, ParamsUserModel,

GetBasketsModel, BasketModel, ItemBasketDeleteModel, GetUsersModel, OrderModel,
    ParamsUserModel,
)

router = APIRouter()  # это роутер, он нужен для FastAPI, чтобы определять эндпоинты


# @router.get("/items", response_model=GetItemsModel)
# def get_items(filters: ParamsItemModel) -> GetItemsModel:
#     items = services.get_items()
#     return GetItemsModel(
#         items=[
#             GetItemModel(item_id=item.id, title=item.title, description=item.description, price=item.price)
#             for item in items
#         ]
#     )
# def authorization(credentials: LoginModel, admin_roots: bool = False) -> tuple[int, str] | bool:
#     current_user = services.login(
#         username=credentials.username,
#         password=credentials.password,
#         admin=credentials.admin,
#     )
#
#     # Это аутентификация
#     if not current_user:
#         return 401, "Unauthorized user"
#
#     # а это авторизация
#     if admin_roots and not current_user.admin:
#         return 403, "Forbidden resource"
#
#     return True
#
# @router.post(
#     "/item/create",
#     response_model=GetItemModel,
#     status_code=status.HTTP_201_CREATED,
#     responses={201: {"model": CreateItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
# )
# def create_item(new_item:CreateItemModel):
#     error = authorization(new_item.credentials, admin_roots= True)
#     if error is not None:
#         status_code, detail = error
#         raise HTTPException(status_code=status_code, detail=detail)
#
#     item = services.create_item(
#         title=new_item.title,
#         description=new_item.description,
#         price=new_item.price,
#         items_repository=ShelveItemsRepository(),
#     )
#     return item
#
# @router.post(
#     "/item/change/description",
#     status_code=status.HTTP_201_CREATED,
#     responses={201: {"model": ChangeItemDescriptionModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
#     # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
# )
# def change_item_description(new_description: ChangeItemDescriptionModel):
#     error = authorization(new_description.credentials)
#     if error is not None:
#         status_code, detail = error
#         raise HTTPException(status_code=status_code, detail=detail)
#
#     services.change_item_description(item_id=new_description.item_id,
#                                      new_description=new_description.new_description,
#                                      repository=ShelveItemsRepository())
#
# @router.post(
#     "/item/change/price",
#     response_model=GetItemModel,
#     status_code=status.HTTP_201_CREATED,
#     responses={201: {"model": GetItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
# )
# def change_item_price(new_item_price: ChangeItemPriceModel):
#     error = authorization(new_item_price.credentials)
#     if error is not None:
#         status_code, detail = error
#         raise HTTPException(status_code=status_code, detail=detail)
#
#     services.change_item_price(item_id=new_item_price.item_id,
#                                new_price=new_item_price.new_price,
#                                repository=ShelveItemsRepository())
#
# # ----------------------------------------------------------BASKET
@router.get(
    path="/baskets",
    response_model=GetBasketsModel,
    status_code=status.HTTP_200_OK,
    responses={200:{"model": GetBasketsModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def get_baskets(id_basket: str | None = None) -> GetBasketsModel:
    filters = {
        "id_basket": id_basket
    }
    baskets = services.get_baskets(filters)
    return GetBasketsModel(baskets = [Basket(id_basket=basket.id_basket, items=basket.items) for basket in baskets])

#
@router.post(
    "/basket/create",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def create_basket() -> str:
    new_basket_id = services.create_basket()
    return new_basket_id

@router.post(
    "/basket/item/add",
    response_model=Basket,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Basket}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def add_item(new_item: AddItemModel) -> Basket:
    item = services.add_item_in_basket(id_basket=new_item.id_basket,
                                        id_item=new_item.id_item,

                                        count=new_item.count)
    return item
#
#
#
@router.delete(
    "/basket/item/delete",
    status_code=status.HTTP_200_OK,
    responses={ 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def delete_basket_item(item: ItemBasketDeleteModel) -> None:
    services.delete_item(id_basket=item.id_basket,id_item=item.id_item)
#
#
@router.delete(
    "/basket/delete",
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def delete_basket(id_basket: str) -> None:
    services.delete_basket(id_basket=id_basket)
#
@router.post(
    "/basket/order",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def order_basket(order: OrderModel) -> str:
    result = services.order_basket(order=order)
    return result
#
@router.get(
    "/basket",
    status_code=status.HTTP_200_OK,
    response_model=Basket,
    responses={200: {"model": GetBasketsModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def get_basket(id_basket: str) -> Basket:
    basket = services.get_basket(id_basket=id_basket)
    if basket is None:
        raise HTTPException(status_code=404, detail="Basket not found")
    return basket

#
# # ----------------------------------регистрация для заказа
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(email: str):
    services.register(email=email)
#
# # --------------------------------пользователи
#
#
#
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
)
def get_users(id: str | None = None,
    username: str | None = None,
    email: str | None = None,
    admin: bool | None = None) -> GetUsersModel:
    filters ={
        "id": id,
        "username": username,
        "email": email,
        "admin": admin

    }
    users = services.get_users(filters)
    return GetUsersModel(users=[user for user in users])

