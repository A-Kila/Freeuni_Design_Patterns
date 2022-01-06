from dataclasses import dataclass, field

from app.core.item.items import Item
from app.core.item.price_calculator import TotalPriceCalculatorTemplate


@dataclass
class Receipt:
    price_calculator: TotalPriceCalculatorTemplate
    items: list[tuple[Item, float]] = field(default_factory=list[tuple[Item, float]])
    sum: float = 0

    def add_item(self, item: Item) -> None:
        final_price = self.price_calculator.get_price(item)
        self.sum += final_price
        self.items.append((item, final_price))
