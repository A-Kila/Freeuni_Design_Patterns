from dataclasses import dataclass

from app.core.item.interactor import ItemResponse
from app.core.item.items import Item
from app.core.item.price_calculator import TotalPriceCalculatorTemplate
from app.core.personel.cash_register import CashRegister, XReport
from app.core.personel.receipt import Receipt


@dataclass
class ReceiptResponse:
    items: list[ItemResponse]
    sum: float


@dataclass
class XReportResponse:
    items: dict[str, int]
    total_revenue: float
    closed_receipts: int


@dataclass
class Cashier:
    price_calculator: TotalPriceCalculatorTemplate

    def __post_init__(self) -> None:
        self._receipt = Receipt(self.price_calculator)

    def add_item_to_receipt(self, item: Item) -> None:
        self._receipt.add_item(item)

    def buy_items_from_receipt(self) -> None:
        CashRegister.getInstance().add_paid_items_from_receipt(self._receipt)

        self._receipt = Receipt(self.price_calculator)

    def get_current_receipt(self) -> ReceiptResponse:
        items_map: map[ItemResponse] = map(
            lambda x: ItemResponse(x[0].name, x[0].price, x[0].units, x[1]),
            self._receipt.items,
        )
        items: list[ItemResponse] = list(items_map)

        return ReceiptResponse(items, self._receipt.sum)


class StoreManager:
    def make_X_report(self) -> XReportResponse:
        X_report: XReport = CashRegister.getInstance().make_X_report()

        return XReportResponse(
            X_report.items, X_report.total_revenue, X_report.closed_receipts
        )
