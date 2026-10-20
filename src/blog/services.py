from uuid import uuid4

from fastapi import HTTPException
from postgres import Postgres
from pydantic import UUID4

from blog.domains import Item, User, Basket, Manager, BasketItem
from blog.repositories import ShelveRepository, Repository
from blog.schemas import OrderModel, ItemBasketDeleteModel, NewManager, CreateItemModel





baskets_repository = PostgresRepository("baskets.db")
users_repository = ShelveRepository("users.db")
items_repository = ShelveRepository("items.db")

# --ITEMS--
def get_items(filters) -> list[Item]:
    return items_repository.get_all(filters)


def create_item(data:CreateItemModel):
    key = str(uuid4())
    item = Item(id=key, title=data.title, description=data.description, price=data.price)
    items_repository.save(key= key, obj=item)



def change_item_description(id_item: str, new_description: str) -> None:
    current_item = items_repository.get(id_item)
    current_item.change_description(new_description)
    items_repository.save(id_item, obj=current_item, overwrite=True)


def change_item_price(id_item: str, new_price: int) -> None:
    current_item = items_repository.get(id_item)
    current_item.change_price(new_price)
    items_repository.save(id_item, obj=current_item, overwrite=True)

# --BASKET--

def get_baskets(filters: dict) -> list[Basket]:

    baskets = baskets_repository.get_all(filters=filters)
    return baskets



def add_item_in_basket(id_item: str, id_basket: str, count: int = 1) -> Basket:
    basket = baskets_repository.get(key=id_basket)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket.add_item(id_item=id_item, count = count)
    baskets_repository.save(key=id_basket, obj=basket)
    return basket

def delete_item(data: ItemBasketDeleteModel) -> None:
    basket = baskets_repository.get(key=data.id_basket)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket.delete_item(id_item=data.id_item)
    baskets_repository.save(key=data.id_basket, obj=basket)
    return basket


def delete_basket(id_basket: str) -> None:
    baskets_repository.delete(id_basket)

def get_basket(id_basket: str) -> Basket | None:
    basket = baskets_repository.get(id_basket)
    return basket

def order_basket(order: OrderModel) -> None:
    if not users_repository.get(order.email):
        raise HTTPException(status_code=401, detail="User not found")

    if not baskets_repository.get(order.id_basket):
        raise HTTPException(status_code=404, detail="Basket not found")

def create_basket() -> None:
    new_basket_id = str(uuid4())
    new_basket = Basket(id_basket=new_basket_id)
    baskets_repository.save(key=new_basket_id, obj=new_basket)






# --USERS--

def register(email: str) :
    id_user = str(uuid4())
    data = User(id=id_user,email=email)
    users_repository.save(key=id_user, obj=data)

def get_users(filters) ->list[User | Manager]:
    return users_repository.get_all(filters)


def add_manager(manager: NewManager) -> None:
    id = str(uuid4())
    data = Manager(id=id, email=manager.email, password=manager.password, username=manager.username, admin=manager.admin)
    users_repository.save(key=id, obj=data)

def login(username: str, password: str, admin: bool) -> Manager | None:
    current_user = users_repository.get_all(filters={"username": username, "password": password, "admin": admin})
    if not current_user:
        return None
    return current_user[0]