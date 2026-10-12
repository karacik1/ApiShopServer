from dataclasses import dataclass, field


@dataclass
class User:
    """Обычный пользователь"""
    id: str
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
class BasketItem:
    id_item: str
    count: int

@dataclass
class Basket:
    id_basket: str
    items: list[BasketItem] = field(default_factory=list)


    def add_item(self, id_item: str, count: int = 1) -> None:
        for bi in self.items:
            if bi.id_item == id_item:
                bi.count += count
                return
        self.items.append(BasketItem(id_item, count))

    def delete_item(self, id_item: str) -> None:
        self.items = [bi for bi in self.items if bi.id_item != id_item]





