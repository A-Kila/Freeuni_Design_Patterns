from abc import ABC, abstractmethod
from dataclasses import dataclass, field

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
    discounts: dict[Item, float] = field(default_factory=lambda: {})

    def get_price(self, item: Item) -> float:
        if item not in self.discounts.keys():
            return self.get_base_price(item)

        assert self.discounts[item] >= 0 and self.discounts[item] <= 1

        return self.get_base_price(item) * (1 - self.discounts[item])


# If needed, we can add price calculator with taxes or something similar
