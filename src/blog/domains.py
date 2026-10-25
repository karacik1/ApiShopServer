from dataclasses import dataclass, field


@dataclass
class User:
    """Обычный пользователь"""
    email: str


@dataclass
class Manager:
    user_id: str
    username: str
    password: str
    is_admin: bool

@dataclass
class Item:

    title: str
    description: str
    price: int



@dataclass
class BasketItem:

    basket_id: str
    item_id: str
    count: int

@dataclass
class Basket:
    id: str
    items: list[BasketItem] = field(default_factory=list)








