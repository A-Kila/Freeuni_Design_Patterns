from fastapi import APIRouter
from fastapi.params import Depends
from starlette.requests import Request

from app.core.facade import ShopService
from app.core.item.interactor import AllItemsResponse, OneItemRequest, OneItemResponse
from app.core.personel.personel import (
    AllXReportResponse,
    OneXReportRequest,
    OneXReportResponse,
    ReceiptResponse,
)

shop_api: APIRouter = APIRouter()


def get_core(request: Request) -> ShopService:
    return request.app.state.service


@shop_api.get("/items")
def get_items(service: ShopService = Depends(get_core)) -> AllItemsResponse:
    return service.get_all_items()


@shop_api.get("/item/{item}")
def get_item(item: str, service: ShopService = Depends(get_core)) -> OneItemResponse:
    return service.get_item(OneItemRequest(item))


@shop_api.post("/item")
def add_item(item: str, service: ShopService = Depends(get_core)) -> None:
    service.add_item_to_shopping_list(item)


@shop_api.post("/buy_items")
def buy_items(service: ShopService = Depends(get_core)) -> None:
    service.buy_items()


@shop_api.get("/receipt")
def get_receipt(service: ShopService = Depends(get_core)) -> ReceiptResponse:
    return service.get_current_receipt()


@shop_api.get("/xreports")
def get_all_X_reports(service: ShopService = Depends(get_core)) -> AllXReportResponse:
    return service.get_all_X_reports()


@shop_api.get("/xreport/{date}")
def get_X_report(
    date: str, service: ShopService = Depends(get_core)
) -> OneXReportResponse:
    return service.get_one_X_report(OneXReportRequest(date))


@shop_api.post("/xreport")
def make_X_report(service: ShopService = Depends(get_core)) -> None:
    service.make_X_report()
