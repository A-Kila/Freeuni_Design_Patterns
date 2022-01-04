from console_logger import RecieptLogger
from items import Item
from price_calculator import DiscountPriceCalculator


class Receipt:
    def __init__(self, price_calculator: DiscountPriceCalculator) -> None:
        self._items: list[Item] = list[Item]()
        self.sum: float = 0
        self.price_calculator = price_calculator

    def add_item(self, item: Item) -> None:
        self.sum += self.price_calculator.get_price(item)
        self._items.append(item)

    def get_items_in_receipt(self) -> list[Item]:
        return self._items

    def print_receipt(self) -> None:
        RecieptLogger(self.price_calculator, self._items, self.sum).log_to_console()
