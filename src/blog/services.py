from uuid import uuid4

import pytest
from fastapi import HTTPException

from blog.domains import  User as UserDomain, Basket as BasketDomain, Manager as ManagerDomain
from blog.models import Item as ItemModel, Basket as BasketModel, User as UserModel
from blog.schemas import (OrderModel, ItemBasketDeleteModel,
                          RepresentBasketModel, FullUser,
                          ParamsUserModel, ChangeItemModel, AddItemModel, Item as ItemDomain, ItemWithoutID, )
# pre-commit run --files src/blog/services.py


# --ITEMS--
class ItemService:
    def __init__(self, items_repository):
        self.items_repository = items_repository

    @pytest.mark.done
    def get_items(self, filters) -> list[ItemModel]:
        return self.items_repository.get_all(filters)

    @pytest.mark.done
    def create_item(self, data:ItemWithoutID):
        self.items_repository.create(data=data)

    @pytest.mark.done
    def delete(self, key: str) -> None:
        self.items_repository.delete(key=key)

    @pytest.mark.done
    def change_item_param(self, data: ChangeItemModel) -> None:
        self.items_repository.update(data)


# --BASKET--
class BasketService:
    def __init__(self, baskets_repository):
        self.baskets_repository = baskets_repository

    @pytest.mark.done
    def get_baskets(self, filters: dict) -> BasketModel:

        baskets = self.baskets_repository.get_all(filters=filters)
        return baskets

    @pytest.mark.done
    def add_item_in_basket(self, item_id: str, basket_id: str, count: int = 1) -> RepresentBasketModel:
        # TODO: хочу что бы сервер сам искал корзину после доавления, а не репозиторий
        basket = self.baskets_repository.get(key=basket_id)
        if not basket:
            raise HTTPException(status_code=404, detail="Basket not found")

        new_basket = self.baskets_repository.add_item(AddItemModel(basket_id=basket_id, item_id=item_id, count=count))
        return new_basket

    @pytest.mark.done
    def delete_item(self, data: ItemBasketDeleteModel) -> None:
        basket = self.baskets_repository.get(key=data.basket_id)
        if not basket:
            raise HTTPException(status_code=404, detail="Basket not found")

        self.baskets_repository.delete_item(item_id=data.item_id, basket_id=data.basket_id)
        return self.baskets_repository.get(key=data.basket_id)

    @pytest.mark.done
    def delete_basket(self, basket_id: str) -> None:
        self.baskets_repository.delete(basket_id)

    def get_basket(self, basket_id: str) -> BasketDomain | None:
        basket = self.baskets_repository.get(basket_id)
        return basket

    # TODO: нужно создать отдельную тиблицу с заказами и пользователями плюс вынести возможно в отдельный метод
    # def order_basket(self, order: OrderModel) -> None:
    #     if not self.users_repository.get(order.email):
    #         raise HTTPException(status_code=401, detail="User not found")
    #
    #     if not self.baskets_repository.get(order.basket_id):
    #         raise HTTPException(status_code=404, detail="Basket not found")

    @pytest.mark.don
    def create_basket(self) -> None:
        self.baskets_repository.create()






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
