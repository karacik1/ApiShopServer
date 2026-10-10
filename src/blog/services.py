from uuid import uuid4

from fastapi import HTTPException

from blog.domains import Item, User, Basket, Manager, BasketItem
from blog.repositories import ItemRepository, BasketsRepository, UsersRepository
from blog.schemas import OrderModel


# --ITEMS--
def get_items(items_repository: ItemRepository) -> list[Item]:
    return items_repository.get_items()


def create_item(
    title: str, description: str, price: int, items_repository: ItemRepository) -> Item:
    item = Item(id=str(uuid4()), title=title, description=description, price=price)
    items_repository.create_item(item=item)
    return item


def change_item_description(item_id: str, new_description: str, repository: ItemRepository) -> None:
    repository.change_item_description(item_id, new_description)


def change_item_price(item_id: str, new_price: int, repository:ItemRepository) -> None:
    repository.change_item_price(item_id, new_price)

# --BASKET--

def get_baskets(repository:BasketsRepository ) -> list[Basket]:
    baskets = repository.get_baskets()
    return baskets



def add_item_in_basket(id_item, repository:BasketsRepository, count, id_basket: str) -> Basket:

    new_item = BasketItem(id_item=id_item,count=count)
    repository.add_item(new_item=new_item, id_basket = id_basket)
    basket = get_basket(id_basket, repository=repository)
    return basket

def delete_item(id_basket: str, item_id: str, repository:BasketsRepository) -> None:
    repository.delete_item(id_basket, item_id)


def delete_basket(id_basket: str, repository:BasketsRepository ) -> None:
    repository.delete_basket(id_basket)

def get_basket(id_basket: str, repository: BasketsRepository) -> Basket | None:
    basket = repository.get_basket(id_basket)
    return basket

def order_basket(order: OrderModel, user_repository: UsersRepository, basket_repository: BasketsRepository) -> str:
    if not user_repository.get_user(order.email):
        raise HTTPException(status_code=404, detail="User not found")

    if not basket_repository.get_basket(order.id_basket):
        raise HTTPException(status_code=404, detail="Basket not found")
    return "Complete"


# --USERS--

def register(user: User, repository: UsersRepository) :
    repository.create_user(user=user)

def get_users(repository: UsersRepository) -> list[User]:
    return repository.get_users()


# def login(users_repository: UsersRepository) -> Manager | None:
#     users = users_repository.get_users()
#     if users:
#         return users[0]
#     return None


def create_basket(repository: BasketsRepository) -> str:
    return repository.create_basket()
