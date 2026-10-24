from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)


class User(Base):
    """Обычный пользователь"""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String)

    manager_profile: Mapped["Manager | None"]  = relationship(back_populates="user")

class BasketItem(Base):
    __tablename__ = "basket_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    basket_id: Mapped[str] = mapped_column(ForeignKey("baskets.id"))
    item_id: Mapped[str] = mapped_column(ForeignKey("items.id"))
    count: Mapped[int] = mapped_column(Integer)

    basket: Mapped["Basket"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship()

class Basket(Base):
    __tablename__ = "baskets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    items: Mapped[list["BasketItem"] | None] = relationship(back_populates="basket")

class Manager(Base):
    __tablename__ = "managers"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    user: Mapped["User"] = relationship(back_populates="manager_profile")



