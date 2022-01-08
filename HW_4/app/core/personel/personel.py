from dataclasses import dataclass
from typing import Optional, Protocol

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
class OneXReportRequest:
    date: str


@dataclass
class OneXReportResponse:
    X_report: Optional[XReportResponse]


@dataclass
class DateReportPair:
    date: str
    report: XReportResponse


@dataclass
class AllXReportResponse:
    X_reports: list[DateReportPair]


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


class IXReportRepository(Protocol):
    def store(self, report: XReport) -> None:
        pass

    def fetch_one(self, date: str) -> Optional[XReport]:
        pass

    def fetch_all(self) -> dict[str, XReport]:
        pass


@dataclass
class StoreManager:
    repo: IXReportRepository

    def _get_X_report_response(self, report: XReport) -> XReportResponse:
        return XReportResponse(
            report.items, report.total_revenue, report.closed_receipts
        )

    def get_one_X_report(self, date_request: OneXReportRequest) -> OneXReportResponse:
        report: Optional[XReport] = self.repo.fetch_one(date_request.date)

        if report is None:
            return OneXReportResponse(None)

        return OneXReportResponse(self._get_X_report_response(report))

    def get_all_X_reports(self) -> AllXReportResponse:
        items: dict[str, XReport] = self.repo.fetch_all()

        responses = list(
            map(
                lambda x: DateReportPair(x[0], self._get_X_report_response(x[1])),
                items.items(),
            )
        )

        print(responses)
        return AllXReportResponse(responses)

    def make_X_report(self) -> None:
        X_report: XReport = CashRegister.getInstance().make_X_report()

        self.repo.store(X_report)
