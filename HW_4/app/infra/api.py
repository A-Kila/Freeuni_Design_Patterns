from fastapi import APIRouter
from starlette.requests import Request

from app.core.shop_core import ShopCore

shop_api: APIRouter = APIRouter()


def get_core(request: Request) -> ShopCore:
    return request.app.state.core


@shop_api.get("/items")
def get_items() -> str:
    return "items"


@shop_api.get("/item/{item}")
def get_item(item: str) -> str:
    return item


@shop_api.post("/item")
def post_item(item: str) -> None:
    pass


@shop_api.post("/buy_items")
def buy_items() -> None:
    pass


@shop_api.get("/receipt")
def get_receipt() -> str:
    return "receipt"


@shop_api.get("/X-report")
def get_X_report() -> str:
    return "X_Report"
