from dataclasses import dataclass
from typing import Optional, Protocol

from app.core.item.items import Item
from app.core.personel.receipt import Receipt


class IDate(Protocol):
    def set_date(self, date_str: str) -> None:
        pass

    def get_date_str(self) -> str:
        pass

    def go_to_next_day(self) -> None:
        pass


@dataclass
class DayCountDate:
    day: int = 0

    def set_date(self, date_str: str) -> None:
        self.day = int(date_str)

    def get_date_str(self) -> str:
        return str(self.day)

    def go_to_next_day(self) -> None:
        self.day += 1


@dataclass
class XReport:
    items: dict[str, int]
    total_revenue: float
    closed_receipts: int
    date: str


class CashRegister:
    _instance: Optional["CashRegister"] = None
    date: IDate = DayCountDate()
    checks_closed: int = 0
    revenue: float = 0
    items_sold: dict[Item, int] = dict[Item, int]()

    @staticmethod
    def getInstance() -> "CashRegister":
        if CashRegister._instance is None:
            CashRegister._instance = CashRegister()

        return CashRegister._instance

    def add_paid_items_from_receipt(self, receipt: Receipt) -> None:
        if receipt.sum == 0:
            return

        self.revenue += receipt.sum

        for item, _ in receipt.items:
            if item in self.items_sold:
                self.items_sold[item] += item.units
            else:
                self.items_sold[item] = item.units

        self.checks_closed += 1

    def make_X_report(self) -> XReport:
        report = XReport(
            dict(map(lambda x: (x[0].name, x[1]), self.items_sold.items())),
            self.revenue,
            self.checks_closed,
            self.date.get_date_str(),
        )
        self.finish_day()

        return report

    def finish_day(self) -> None:
        self.checks_closed = 0
        self.revenue = 0
        self.items_sold.clear()

        self.date.go_to_next_day()
