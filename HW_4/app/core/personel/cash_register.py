from typing import Optional

from app.core.item.items import Item
from app.core.personel.receipt import Receipt


class XReport:
    def __init__(
        self, items: dict[Item, int], sum: float, closed_receipts: int
    ) -> None:
        self.items = dict[str, int]()

        for item, units in items.items():
            self.items[item.name] = units

        self.total_revenue = sum
        self.closed_receipts = closed_receipts


class CashRegister:
    _instance: Optional["CashRegister"] = None
    day: int = 0
    checks_closed: int = 0
    revenue: float = 0
    items_sold: dict[Item, int] = dict[Item, int]()

    @staticmethod
    def getInstance() -> "CashRegister":
        if CashRegister._instance is None:
            CashRegister._instance = CashRegister()

        return CashRegister._instance

    def add_paid_items_from_receipt(self, receipt: Receipt) -> None:
        print(receipt, receipt.sum)
        self.revenue += receipt.sum

        for item, _ in receipt.items:
            if item in self.items_sold:
                self.items_sold[item] += item.units
            else:
                self.items_sold[item] = item.units

        self.checks_closed += 1

    def make_X_report(self) -> XReport:
        return XReport(self.items_sold, self.revenue, self.checks_closed)

    def finish_day(self) -> None:
        self.checks_closed = 0
        self.revenue = 0
        self.items_sold.clear()

        self.day += 1
