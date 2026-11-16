from fastapi import Depends

from blog.db import SessionLocal
from blog.repositories import PostgresItemRepository, PostgresBasketRepository, PostgresManagerRepository, \
    PostgresUserRepository
from blog.services import ItemService, BasketService, UserService, ManagerService


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_item_service(session=Depends(get_session)):
    repository = PostgresItemRepository(session)
    return ItemService(repository)


def get_basket_service(session=Depends(get_session)):
    repository = PostgresBasketRepository(session)
    return BasketService(repository)

def get_manager_service(session=Depends(get_session)):
    repository = PostgresManagerRepository(session)
    return ManagerService(repository)

def get_user_service(session=Depends(get_session)):
    repository = PostgresUserRepository(session)
    return UserService(repository)
