from typing import Optional

from console_logger import CashReportLogger
from items import Item
from receipt import Receipt


class CashRegister:
    _instance: Optional["CashRegister"] = None
    revenue: float = 0
    items_sold: dict[Item, int] = dict[Item, int]()

    @staticmethod
    def getInstance() -> "CashRegister":
        if CashRegister._instance is None:
            CashRegister._instance = CashRegister()

        return CashRegister._instance

    def add_paid_items_from_receipt(self, receipt: Receipt) -> None:
        self.revenue += receipt.sum

        for item in receipt.get_items_in_receipt():
            if item in self.items_sold:
                self.items_sold[item] += item.units
            else:
                self.items_sold[item] = item.units

    def clear_cash_register(self) -> None:
        self.revenue = 0
        self.items_sold.clear()

    def print_register_info(self) -> None:
        CashReportLogger(self.items_sold, self.revenue).log_to_console()
