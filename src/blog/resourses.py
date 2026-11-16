from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi import Query

from blog import services, repositories
from blog.db import SessionLocal
from blog.dependencies import get_item_service, get_basket_service, get_user_service
from blog.domains import Basket, Manager, User
from blog.schemas import (
    GetItemsModel,
    LoginModel,
    ErrorModel, AddItemModel, GetBasketsModel,
    ItemBasketDeleteModel, GetUsersModel, OrderModel,
    ParamsUserModel, ParamsItemModel, ParamsBasketModel, RegisterUserModel, RepresentBasketModel, ItemWithoutID,
    ChangeItemModel,
)

router = APIRouter()  # это роутер, он нужен для FastAPI, чтобы определять эндпоинты


# ---------------------AUTORIZATION AND ADMIN ROOTS
def authorization(credentials: LoginModel) -> Manager:
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
    )

    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized user")  # Прерываем запрос
    return current_user

def require_admin(user: Manager = Depends(authorization)) -> None:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden resource")
    return None

def require_manager(_: Manager = Depends(authorization)) -> None:
    return None




# ---------------------------ITEMS
@router.get("/items",
            status_code=status.HTTP_200_OK,)
def get_items(filters: Annotated[ParamsItemModel, Query()], service: services.ItemService = Depends(get_item_service)) -> GetItemsModel:
    items = service.get_items(filters.model_dump(exclude_none=True))
    return GetItemsModel(items=[item for item in items])

@router.post(
    "/item/create",
    status_code=status.HTTP_201_CREATED,
    responses={ 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def create_item(item: ItemWithoutID, _ = Depends(require_admin), service: services.ItemService = Depends(get_item_service)) :
    service.create_item(item)
    return "done"

@router.patch(
    "/item/change/description",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={ 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def change_item_description(data: ChangeItemModel, _ = Depends(require_manager), service: services.ItemService = Depends(get_item_service)) -> None:
    service.change_item_param(data=data)

@router.patch(
    "/item/change/price",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def change_item_price(data: ChangeItemModel, _ = Depends(require_manager), service: services.ItemService = Depends(get_item_service)) -> None:
    service.change_item_param(data=data)


# # ----------------------------------------------------------BASKET
@router.get(
    path="/baskets",
    response_model=GetBasketsModel,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": GetBasketsModel}}
)
def get_baskets(filters: Annotated[ParamsBasketModel, Query()], service: services.BasketService = Depends(get_basket_service)) -> GetBasketsModel:
    baskets = service.get_baskets(filters.model_dump(exclude_none=True))
    return GetBasketsModel(baskets=[Basket(id=basket.id, items=basket.items) for basket in baskets])


#
@router.post(
    "/basket/create",
    status_code=status.HTTP_201_CREATED,
    responses={}
)
def create_basket(service: services.BasketService = Depends(get_basket_service)) -> None:
    service.create_basket()



@router.patch(
    "/basket/item/add",
    response_model=RepresentBasketModel,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Basket}, 404:{"model": ErrorModel}},
)
def add_item(new_item: AddItemModel, service: services.BasketService = Depends(get_item_service)) -> RepresentBasketModel:
    item = service.add_item_in_basket(basket_id=new_item.basket_id,
                                       item_id=new_item.item_id,
                                       count=new_item.count)
    return item


@router.delete(
    "/basket/item/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404:{"model": ErrorModel}}
)
def delete_basket_item(data: Annotated[ItemBasketDeleteModel, Query()], service: services.BasketService = Depends(get_basket_service)) -> None:
    service.delete_item(data.model_dump())

@router.delete(
    "/basket/delete",
    status_code=status.HTTP_204_NO_CONTENT,

)
def delete_basket(basket_id: str, service: services.BasketService = Depends(get_basket_service)) -> None:
    service.delete_basket(basket_id=basket_id)


@router.post(
    "/basket/order",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorModel}, 404:{"model": ErrorModel}}
)
def order_basket(order: OrderModel, service: services.BasketService = Depends(get_basket_service)):
    service.order_basket(order=order)





# ----------------------------------регистрация для заказа
@router.post(
    "/register",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"model": ErrorModel}}
)
def register(data: RegisterUserModel, service: services.UserService = Depends(get_user_service)) -> None:
    service.register(email=data.email)




# --------------------------------пользователи
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    responses={200: {"model": GetUsersModel}}
)
def get_users(
    filters: Annotated[ParamsUserModel, Query()], service: services.UserService = Depends(get_user_service)) -> GetUsersModel:
    users = service.get_users(filters.model_dump(exclude_none=True))
    return GetUsersModel(users=[user for user in users])
