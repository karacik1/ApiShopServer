from uuid import uuid4

from fastapi import HTTPException

from blog.domains import Item, User as UserDomain, Basket, Manager
from blog.models import User as UserModel
from blog.repositories import PostgresUserRepository
from blog.schemas import OrderModel, ItemBasketDeleteModel, NewManager, CreateItemModel, RepresentBasketModel

baskets_repository = None
items_repository = None

# --ITEMS--
def get_items(filters) -> list[Item]:
    return items_repository.get_all(filters)


def create_item(data:CreateItemModel):
    key = str(uuid4())
    item = Item(id=key, title=data.title, description=data.description, price=data.price)
    items_repository.save(key= key, obj=item)



def change_item_description(item_id: str, new_description: str) -> None:
    current_item = items_repository.get(key=item_id)
    current_item.change_description(new_description)
    items_repository.save(item_id, obj=current_item, overwrite=True)


def change_item_price(item_id: str, new_price: int) -> None:
    current_item = items_repository.get(item_id)
    current_item.change_price(new_price)
    items_repository.save(item_id, obj=current_item, overwrite=True)

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
    def __init__(self, users_repository) -> None:
        self.users_repository = users_repository


    def register(self, email: str) :
        data = UserDomain(email=email)
        self.users_repository.create(obj=data)

    def get_users(self, filters) ->list[UserDomain | Manager]:
        return self.users_repository.get_all(filters)


    def add_manager(self, manager: NewManager) -> None:
        id = str(uuid4())
        data = Manager(id=id, email=manager.email, password=manager.password, username=manager.username, admin=manager.admin)
        self.users_repository.save(key=id, obj=data)

    def login(self, username: str, password: str) -> Manager | None:
        current_user = self.users_repository.get_all(filters={"username": username, "password": password})
        if not current_user:
            return None
        return current_user[0]