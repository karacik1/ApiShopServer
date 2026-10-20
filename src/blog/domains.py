from dataclasses import dataclass, field


@dataclass
class User:
    """Обычный пользователь"""
    id: str
    email: str


@dataclass
class Manager:
    id: str
    user_id: str
    username: str
    password: str
    is_admin: bool

@dataclass
class Item:
    id: str
    title: str
    description: str
    price: int

    def change_description(self, new_description):
        self.description = new_description


    def change_price(self, new_price):
        self.price = new_price


@dataclass
class BasketItem:
    id: str
    basket_id: str
    item_id: str
    count: int

@dataclass
class Basket:
    id: str
    items: list[BasketItem] = field(default_factory=list)








