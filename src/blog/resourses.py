from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi import Query

from blog import services
from blog.domains import Basket, Manager, User
from blog.schemas import (
    GetItemModel,
    GetItemsModel,
    LoginModel,
    ErrorModel, CreateItemModel, ChangeItemDescriptionModel, ChangeItemPriceModel, AddItemModel, GetBasketsModel,
    ItemBasketDeleteModel, GetUsersModel, OrderModel,
    ParamsUserModel, ParamsItemModel, ParamsBasketModel,
)


router = APIRouter()  # это роутер, он нужен для FastAPI, чтобы определять эндпоинты

@router.get("/items")
def get_items(filters: Annotated[ParamsItemModel, Query()],
) -> GetItemsModel:
    items = services.get_items(filters.model_dump(exclude_none=True))
    return GetItemsModel(items=[item for item in items])


def authorization(credentials: LoginModel) -> Manager:
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        admin=credentials.admin,
    )

    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized user")  # Прерываем запрос
    return current_user

def require_admin(user: Manager = Depends(authorization)) -> None:
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden resource")
    return None

def require_manager(_: Manager = Depends(authorization)) -> None:
    return None

@router.post(
    "/item/create",
    status_code=status.HTTP_201_CREATED
)
def create_item(item: CreateItemModel, _ = Depends(require_admin)) :
    services.create_item(item)
    return "done"


@router.post(
    "/item/change/description",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={ 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def change_item_description(data: ChangeItemDescriptionModel, _ = Depends(require_manager)) -> None:
    services.change_item_description(id_item=data.id_item,
                                     new_description=data.new_description,
                                     )

@router.post(
    "/item/change/price",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def change_item_price(data: ChangeItemPriceModel, _ = Depends(require_manager)) -> None:
    services.change_item_price(id_item=data.id_item,
                               new_price=data.new_price,
                               )


# # ----------------------------------------------------------BASKET
@router.get(
    path="/baskets",
    response_model=GetBasketsModel,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": GetBasketsModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def get_baskets(filters: Annotated[ParamsBasketModel, Query()]) -> GetBasketsModel:

    baskets = services.get_baskets(filters.model_dump(exclude_none=True))
    return GetBasketsModel(baskets=[Basket(id_basket=basket.id_basket, items=basket.items) for basket in baskets])


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


@router.delete(
    "/basket/item/delete",
    status_code=status.HTTP_200_OK,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def delete_basket_item(data: Annotated[ItemBasketDeleteModel, Query()]) -> None:
    services.delete_item(data.model_dump())

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
def get_users(
    filters: Annotated[ParamsUserModel, Query()],) -> GetUsersModel:
    users = services.get_users(filters.model_dump(exclude_none=True))
    return GetUsersModel(users=[user for user in users])
