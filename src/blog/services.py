from uuid import uuid4

import pytest
from fastapi import HTTPException

from blog.domains import Item as ItemDomain, User as UserDomain, Basket, Manager as ManagerDomain
from blog.models import Item as ItemModel
from blog.schemas import (OrderModel, ItemBasketDeleteModel,
                          RepresentBasketModel, FullUser,
                          ParamsUserModel, ChangeItemModel)

baskets_repository = None
# pre-commit run --files src/blog/services.py


# --ITEMS--
class ItemService:
    def __init__(self, items_repository):
        self.items_repository = items_repository

    @pytest.mark.done
    def get_items(self, filters) -> list[ItemModel]:
        return self.items_repository.get_all(filters)

    @pytest.mark.done
    def create_item(self, data:ItemDomain):
        self.items_repository.create(data=data)

    @pytest.mark.done
    def delete(self, key: str) -> None:
        self.items_repository.delete(key=key)

    @pytest.mark.done
    def change_item_param(self, data: ChangeItemModel) -> None:
        self.items_repository.update(data)


# --BASKET--

def get_baskets(filters: dict) -> list[Basket]:

    baskets = baskets_repository.get_all(filters=filters)
    return baskets



def add_item_in_basket(item_id: str, basket_id: str, count: int = 1) -> RepresentBasketModel:
    basket = baskets_repository.get(key=basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket.add_item(item_id=item_id, count = count)
    baskets_repository.save(key=basket_id, obj=basket)
    return basket

def delete_item(data: ItemBasketDeleteModel) -> None:
    basket = baskets_repository.get(key=data.basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket.delete_item(item_id=data.item_id)
    baskets_repository.save(key=data.basket_id, obj=basket)
    return basket


def delete_basket(basket_id: str) -> None:
    baskets_repository.delete(basket_id)

def get_basket(basket_id: str) -> Basket | None:
    basket = baskets_repository.get(basket_id)
    return basket

def order_basket(order: OrderModel) -> None:
    if not users_repository.get(order.email):
        raise HTTPException(status_code=401, detail="User not found")

    if not baskets_repository.get(order.basket_id):
        raise HTTPException(status_code=404, detail="Basket not found")

def create_basket() -> None:
    new_basket_id = str(uuid4())
    new_basket = Basket(id=new_basket_id)
    baskets_repository.save(key=new_basket_id, obj=new_basket)






# --USERS--
class UserService:
    def __init__(self, users_repository):
        self.users_repository = users_repository

    @pytest.mark.done
    def register(self, email: str) :
        data = UserDomain(email=email)
        self.users_repository.create(obj=data)

    @pytest.mark.done
    def get_users(self, filters) ->list[FullUser]:
        return self.users_repository.get_all(filters=filters)

    @pytest.mark.done
    def login(self, email: str) -> UserDomain | None:
        filter = ParamsUserModel(email=email)
        current_user = self.users_repository.get_all(filters=filter)
        if not current_user:
            return None
        return UserDomain(email=current_user[0].email)

class ManagerService:
    def __init__(self, managers_repository) -> None:
        self.managers_repository = managers_repository

    @pytest.mark.done
    def add_manager(self, manager: ManagerDomain) -> None:
        self.managers_repository.create(data=manager)
