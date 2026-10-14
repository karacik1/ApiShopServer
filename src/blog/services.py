from uuid import uuid4

from fastapi import HTTPException

from blog.domains import Item, User, Basket, Manager, BasketItem
from blog.repositories import ShelveRepository, Repository
from blog.schemas import OrderModel

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

def get_baskets(filters: dict) -> list[Basket]:
    filters = {
        k: v for k, v in {
            "id_basket": filters["id_basket"],
        }.items() if v is not None
    }
    baskets = baskets_repository.get_all(filters=filters)
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

def order_basket(order: OrderModel) -> str:
    if not users_repository.get(order.email):
        raise HTTPException(status_code=404, detail="User not found")

    if not baskets_repository.get(order.id_basket):
        raise HTTPException(status_code=404, detail="Basket not found")
    return "Complete"


# --USERS--

def register(email: str) :
    id_user = str(uuid4())
    data = User(id=id_user,email=email)
    users_repository.save(key=id_user, obj=data)

def get_users(filters) ->list[User | Manager]:
    filters = {
        k: v for k, v in {
            "id": id,

            "email": filters["email"],

            "admin": filters["admin"],
        }.items() if v is not None
    }
    return users_repository.get_all(filters)


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
