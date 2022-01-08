from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from app.core.item.items import Item


class TotalPriceCalculatorTemplate(ABC):
    def get_base_price(self, item: Item) -> float:
        return float(item.price * item.units)

    @abstractmethod
    def get_price(self, item: Item) -> float:
        pass


class TotalPriceCalculator(TotalPriceCalculatorTemplate):
    def get_price(self, item: Item) -> float:
        return self.get_base_price(item)


# We do not need this part in this assignment
class IDiscountsRepository(Protocol):
    def get_discounted_items(self) -> set[str]:
        pass

    def get_discount(self, key: str) -> float:
        pass


@dataclass
class DiscountPriceCalculator(TotalPriceCalculatorTemplate):
    discounts: IDiscountsRepository

    def get_price(self, item: Item) -> float:
        if item.key not in self.discounts.get_discounted_items():
            return self.get_base_price(item)

        discount: float = self.discounts.get_discount(item.name)

        assert discount >= 0 and discount <= 1

        return self.get_base_price(item) * (1 - discount)


# If needed, we can add price calculator with taxes or something similar
