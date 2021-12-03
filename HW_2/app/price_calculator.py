from abc import ABC, abstractmethod
from dataclasses import dataclass

from items import Item


class TotalPriceCalculatorTemplate(ABC):
    def get_base_price(self, item: Item) -> float:
        return item.price * item.units

    @abstractmethod
    def get_price(self, item: Item) -> float:
        pass


class TotalPriceCalculator(TotalPriceCalculatorTemplate):
    def get_price(self, item: Item) -> float:
        return self.get_base_price(item)


@dataclass
class DiscountPriceCalculator(TotalPriceCalculatorTemplate):
    _discounts: dict[Item, float] = {}

    def add_discount_0_to_1(self, item: Item, discount: float) -> None:
        assert discount >= 0 and discount <= 1

        self._discounts[item] = discount

    def get_price(self, item: Item) -> float:
        return self.get_base_price(item) * (1 - self._discounts[item])


# If needed, we can add price calculator with taxes or something similar
