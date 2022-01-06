from fastapi import FastAPI

from app.core.facade import ShopService
from app.core.item.interactor import IItemRepository
from app.core.item.items import Item
from app.infra.fastapi.api import shop_api
from app.infra.in_memory.in_memory import dummyMemory


def setup() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(shop_api)
    app.state.service = ShopService.create(setup_repository())

    return app


def setup_repository() -> IItemRepository:
    repo = dummyMemory()
    repo.create(Item("item1", 9.99))
    repo.create(Item("item2", 19.99))

    return repo
