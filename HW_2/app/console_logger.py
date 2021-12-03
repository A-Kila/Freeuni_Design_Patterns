from dataclasses import dataclass
from typing import Protocol

from items import Item
from price_calculator import DiscountPriceCalculator


class ConsoleLoggerStrategy(Protocol):
    def log_to_console(self) -> None:
        pass


@dataclass
class CashReportLogger:
    _items_sold: dict[Item, int]
    _revenue: float

    def log_to_console(self) -> None:
        report: str = "Name    Sold\n"

        for item, units in self._items_sold.items():
            report += f"{item.name}    {units}\n"

        report += f"Total Revenue: {self._revenue}"

        print(report)


@dataclass
class RecieptLogger:
    _price_calculator: DiscountPriceCalculator
    _items: list[Item]
    _sum: float

    def log_to_console(self) -> None:
        recipt: str = "Name    Units    Price    Total\n"

        for item in self._items:
            recipt += f"{item.name}    {item.units}    {item.price}    {self._price_calculator.get_price(item)}\n"

        recipt += f"Sum: {self._sum}"

        print(recipt)
