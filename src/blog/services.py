from uuid import uuid4

from fastapi import HTTPException

from blog.domains import Item, User, Basket, Manager, BasketItem
from blog.repositories import ShelveRepository, Repository
from blog.schemas import OrderModel, RegisterUserModel

baskets_repository = ShelveRepository("baskets.db")
users_repository = ShelveRepository("users.db")
items_repository = ShelveRepository("items.db")

# --ITEMS--
def get_items() -> list[Item]:
    return items_repository.get_all()


def create_item(
    title: str, description: str, price: int) -> Item:
    item = Item(id=str(uuid4()), title=title, description=description, price=price)
    items_repository.create_item(item=item)
    return item


def change_item_description(item_id: str, new_description: str) -> None:
    items_repository.change_item_description(item_id, new_description)


def change_item_price(item_id: str, new_price: int) -> None:
    items_repository.change_item_price(item_id, new_price)

# --BASKET--

def get_baskets() -> list[Basket]:
    baskets = baskets_repository.get_all()
    return baskets



def add_item_in_basket(id_item: str, id_basket: str, count: int = 1) -> Basket:
    basket = baskets_repository.get(key=id_basket)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket.add_item(id_item=id_item, count = count)
    baskets_repository.save(key=id_basket, obj=basket)
    return basket

def delete_item(id_basket: str, id_item: str) -> None:
    basket = baskets_repository.get(key=id_basket)
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found")

    basket.delete_item(id_item=id_item)
    baskets_repository.save(key=id_basket, obj=basket)
    return basket


def delete_basket(id_basket: str) -> None:
    baskets_repository.delete(id_basket)

def get_basket(id_basket: str) -> Basket | None:
    basket = baskets_repository.get(id_basket)
    return basket

def order_basket(order: OrderModel, basket_repository: Repository) -> str:
    if not users_repository.get(order.email):
        raise HTTPException(status_code=404, detail="User not found")

    if not basket_repository.get(order.id_basket):
        raise HTTPException(status_code=404, detail="Basket not found")
    return "Complete"


# --USERS--

def register(email: str) :
    id_user = str(uuid4())
    data = User(id=id_user,email=email)
    users_repository.save(key=id_user, obj=data)

def get_users() ->list[User]:
    return users_repository.get_all()


# def login(users_repository: UsersRepository) -> Manager | None:
#     users = users_repository.get_users()
#     if users:
#         return users[0]
#     return None


def create_basket() -> str:
    new_basket_id = str(uuid4())
    new_basket = Basket(id_basket=new_basket_id)
    baskets_repository.save(key=new_basket_id, obj=new_basket)
    return new_basket_id
