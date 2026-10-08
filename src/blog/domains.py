from dataclasses import dataclass


@dataclass
class User:
    """Обычный пользователь"""
    id: str


@dataclass
class Manager(User):
    username: str
    password: str
    admin: bool

@dataclass
class Item:
    """Сущность статьи"""
    id: str
    title: str
    description: str
    price: int

@dataclass
class Basket:
    id: str
    id_user: str
    id_item: str
    count: int

