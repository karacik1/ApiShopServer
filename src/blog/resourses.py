from typing import Literal

from fastapi import APIRouter, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from blog.domains import Manager, Basket
from blog.schemas import (
    GetItemModel,
    GetItemsModel,
    GetBasketsModel,
    BasketModel,
    LoginModel,
    LoginUserModel,
    ErrorModel, CreateItemModel, ChangeItemDescriptionModel, ChangeItemPriceModel, BasketModel, SaveItemModel,
    ItemBasketDeleteModel,
)
from blog import services
from blog.repositories import ShelveItemsRepository, ShelveBasketsRepository, ShelveManagersRepository

router = APIRouter()  # это роутер, он нужен для FastAPI, чтобы определять эндпоинты


@router.get("/items", response_model=GetItemsModel)
def get_items() -> GetItemsModel:
    items = services.get_items(items_repository=ShelveItemsRepository())
    return GetItemsModel(
        items=[
            GetItemModel(item_id=item.id, title=item.title, description=item.description, price=item.price)
            for item in items
        ]
    )
def authorization(credentials: LoginModel, admin_roots: bool = False) -> tuple[int, str] | None:
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        admin=credentials.admin,
        users_repository=ShelveManagersRepository(),
    )

    # Это аутентификация
    if not current_user:
        return 401, "Unauthorized user"

    # а это авторизация
    if admin_roots and not current_user.admin:
        return 403, "Forbidden resource"

    return None

@router.post(
    "/item/create",
    response_model=GetItemModel,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": CreateItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def create_item(new_item:CreateItemModel):
    error = authorization(new_item.credentials, admin_roots= True)
    if error is not None:
        status_code, detail = error
        raise HTTPException(status_code=status_code, detail=detail)

    item = services.create_item(
        title=new_item.title,
        description=new_item.description,
        price=new_item.price,
        items_repository=ShelveItemsRepository(),
    )
    return item






@router.post(
    "/item/change/description",
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": ChangeItemDescriptionModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
)
def change_item_description(new_description: ChangeItemDescriptionModel):
    error = authorization(new_description.credentials)
    if error is not None:
        status_code, detail = error
        raise HTTPException(status_code=status_code, detail=detail)

    services.change_item_description(item_id=new_description.item_id,
                                     new_description=new_description.new_description,
                                     repository=ShelveItemsRepository())

@router.post(
    "/item/change/price",
    response_model=GetItemModel,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": GetItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def change_item_price(new_item_price: ChangeItemPriceModel):
    error = authorization(new_item_price.credentials)
    if error is not None:
        status_code, detail = error
        raise HTTPException(status_code=status_code, detail=detail)

    services.change_item_price(item_id=new_item_price.item_id,
                               new_price=new_item_price.new_price,
                               repository=ShelveItemsRepository())


@router.get(
    path="/baskets",
    response_model=GetBasketsModel,
    status_code=status.HTTP_200_OK,
    responses={200:{"model": GetBasketsModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def get_baskets() -> GetBasketsModel:
    baskets = services.get_baskets(repository=ShelveBasketsRepository())
    return GetBasketsModel(
        basket=[
            BasketModel(id_basket=basket.id, id_user=basket.id_user, id_item=basket.id_item, count=basket.count)
            for basket in baskets])

@router.post(
    "/basket/item/save",
    response_model=Basket,
    status_code=status.HTTP_200_OK,
    responses={200: {"model": Basket}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def save_item(new_item: SaveItemModel) -> Basket:
    item = services.save_item_in_basket(id_user=new_item.id_user,
                                        id_item=new_item.id_item,
                                        repository=ShelveBasketsRepository(),
                                        count=new_item.count)
    return item

@router.delete(
    "/basket/item/delete",
    status_code=status.HTTP_200_OK,
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def delete_basket_item(item: ItemBasketDeleteModel) -> None:
    services.delete_item(id_user=item.id_user,item_id=item.id_item,repository=ShelveBasketsRepository())


@router.get(
    "/basket/delete",
    responses={401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def delete_basket(id_user: str) -> None:
    services.delete_basket(id_user=id_user, repository=ShelveBasketsRepository())


@router.get(
    "/basket",
    status_code=status.HTTP_200_OK,
    response_model=GetBasketsModel,
    responses={200: {"model": GetBasketsModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}}
)
def get_basket(id_user: str) -> GetBasketsModel:
    baskets = services.get_basket(id_user=id_user, repository=ShelveBasketsRepository())
    return GetBasketsModel(
        basket=[BasketModel(id_basket=basket.id, id_user=basket.id_user,id_item=basket.id_item, count=basket.count)
                for basket in baskets]
    )




