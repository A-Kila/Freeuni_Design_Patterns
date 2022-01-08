from fastapi import FastAPI

from app.core.facade import ShopService
from app.core.item.interactor import IItemRepository
from app.core.item.items import Item, Pack
from app.core.personel.personel import IXReportRepository
from app.infra.fastapi.api import shop_api
from app.infra.in_memory.items_repository import SqliteItemRepository
from app.infra.in_memory.report_repository import SqliteXReportRepository

DB_NAME = "database.db"


def setup() -> FastAPI:
    app: FastAPI = FastAPI()
    app.include_router(shop_api)
    app.state.service = ShopService.create(
        setup_item_repository(), setup_X_report_repository()
    )

    return app


def setup_item_repository() -> IItemRepository:
    repo = SqliteItemRepository(DB_NAME)

    beer = Item("Beer", 4.99)
    chacha = Item("Chacha", 19.99)

    repo.create(beer)
    repo.create(chacha)
    repo.create(Pack(beer, 6))
    repo.create(Pack(chacha, 1000))

    return repo


def setup_X_report_repository() -> IXReportRepository:
    return SqliteXReportRepository(DB_NAME)
