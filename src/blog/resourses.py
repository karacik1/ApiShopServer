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
from blog.repositories import ShelveItemsRepository, ShelveUsersRepository, ShelveBasketsRepository

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

@router.post(
    "/item/create",
    response_model=GetItemModel,
    status_code=status.HTTP_201_CREATED,  # 201 статус код потому что мы создаем объект – стандарт HTTP
    responses={201: {"model": CreateItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
)
def create_item(new_item:CreateItemModel):  # credentials – тело с логином и паролем. Обычно аутентификация выглядит сложнее, но для нашего случая пойдет и так.
    # authorization(credentials)
    item = services.create_item(
        title=new_item.title,
        description=new_item.description,
        price=new_item.price,
        items_repository=ShelveItemsRepository(),
    )
    return item

def authorization(credentials: LoginModel):
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        users_repository=ShelveUsersRepository(),
    )

    # Это аутентификация
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )
    # а это авторизация
    if not isinstance(current_user, Manager):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
        )



@router.post(
    "/item/change/description",
    status_code=status.HTTP_201_CREATED,  # 201 статус код потому что мы создаем объект – стандарт HTTP
    responses={201: {"model": ChangeItemDescriptionModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
)
def change_item_description(new_description: ChangeItemDescriptionModel):
    services.change_item_description(item_id=new_description.item_id,
                                     new_description=new_description.new_description,
                                     repository=ShelveItemsRepository())

@router.post(
    "/item/change/price",
    response_model=GetItemModel,
    status_code=status.HTTP_201_CREATED,  # 201 статус код потому что мы создаем объект – стандарт HTTP
    responses={201: {"model": GetItemModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
    # Это нужно для сваггера. Мы перечисляем ответы эндпоинта, чтобы получить четкую документацию.
)
def change_item_price(new_item_price: ChangeItemPriceModel):
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