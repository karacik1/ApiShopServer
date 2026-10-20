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
    ParamsUserModel, ParamsItemModel, ParamsBasketModel, RegisterUserModel, RepresentBasketModel,
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
def get_items(filters: Annotated[ParamsItemModel, Query()],
) -> GetItemsModel:
    items = services.get_items(filters.model_dump(exclude_none=True))
    return GetItemsModel(items=[item for item in items])

@router.post(
    "/item/create",
    status_code=status.HTTP_201_CREATED,
    responses={ 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def create_item(item: CreateItemModel, _ = Depends(require_admin)) :
    services.create_item(item)
    return "done"

@router.patch(
    "/item/change/description",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={ 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def change_item_description(data: ChangeItemDescriptionModel, _ = Depends(require_manager)) -> None:
    services.change_item_description(new_description=data.new_description,
                                     )

@router.patch(
    "/item/change/price",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def change_item_price(data: ChangeItemPriceModel, _ = Depends(require_manager)) -> None:
    services.change_item_price(new_price=data.new_price,
                               )


# # ----------------------------------------------------------BASKET
@router.get(
    path="/baskets",
    response_model=GetBasketsModel,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": GetBasketsModel}}
)
def get_baskets(filters: Annotated[ParamsBasketModel, Query()]) -> GetBasketsModel:
    baskets = services.get_baskets(filters.model_dump(exclude_none=True))
    return GetBasketsModel(baskets=[Basket(id=basket.id, items=basket.items) for basket in baskets])


#
@router.post(
    "/basket/create",
    status_code=status.HTTP_201_CREATED,
    responses={}
)
def create_basket() -> None:
    services.create_basket()



@router.patch(
    "/basket/item/add",
    response_model=RepresentBasketModel,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Basket}, 404:{"model": ErrorModel}},
)
def add_item(new_item: AddItemModel) -> RepresentBasketModel:
    item = services.add_item_in_basket(basket_id=new_item.basket_id,
                                       item_id=new_item.item_id,

                                       count=new_item.count)
    return item


@router.delete(
    "/basket/item/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404:{"model": ErrorModel}}
)
def delete_basket_item(data: Annotated[ItemBasketDeleteModel, Query()]) -> None:
    services.delete_item(data.model_dump())

@router.delete(
    "/basket/delete",
    status_code=status.HTTP_204_NO_CONTENT,

)
def delete_basket(basket_id: str) -> None:
    services.delete_basket(basket_id=basket_id)

@router.post(
    "/basket/order",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": ErrorModel}, 404:{"model": ErrorModel}}
)
def order_basket(order: OrderModel):
    services.order_basket(order=order)





# ----------------------------------регистрация для заказа
@router.post(
    "/register",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={401: {"model": ErrorModel}}
)
def register(data: RegisterUserModel) -> None:
    services.register(email=data.email)




# --------------------------------пользователи
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    responses={200: {"model": GetUsersModel}}
)
def get_users(
    filters: Annotated[ParamsUserModel, Query()],) -> GetUsersModel:
    users = services.get_users(filters.model_dump(exclude_none=True))
    return GetUsersModel(users=[user for user in users])

