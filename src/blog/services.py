from uuid import uuid4

from blog.domains import Item, User, Basket
from blog.repositories import ItemRepository, UserRepository, BasketsRepository

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


def save_item_in_basket(id_user, id_item, repository:BasketsRepository, count ) -> Basket:
    new_basket = Basket(id=str(uuid4()),
                        id_user=id_user,
                        id_item=id_item,
                        count=count)
    repository.add_item(new_basket)
    return new_basket


def delete_item(basket_id: Basket, item_id, repository:BasketsRepository ) -> None:
    repository.delete_item(basket_id, item_id)


def delete_basket(id_basket, repository:BasketsRepository ) -> None:
    repository.delete_basket(id_basket)




# --USERS--
def login(
    username: str, password: str, users_repository: UserRepository) -> User | None:
    users = users_repository.get_users(username=username, password=password)
    if users:
        return users[0]
