from dataclasses import dataclass


@dataclass
class User:
    """Обычный пользователь"""
    email: str


@dataclass
class Manager(User):
    username: str
    password: str
    admin: bool

@dataclass
class Item:
    id: str
    title: str
    description: str
    price: int


@dataclass
class Basket:
    id_basket: str
    items: list[BasketItem]

@dataclass
class BasketItem:
    id_item: str
    count: int

