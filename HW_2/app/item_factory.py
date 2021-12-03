from dataclasses import dataclass, field
from random import choice

from items import (
    BabyFood,
    Car,
    CarBatch,
    Chacha,
    ChachaPackCarCollection,
    ChachaSixPack,
    Item,
)


@dataclass
class Shop:
    items: list[Item] = field(
        default_factory=lambda: [
            Chacha(),
            BabyFood(),
            Car(),
            ChachaSixPack(),
            CarBatch(),
            ChachaPackCarCollection(),
        ]
    )

    def get_n_items(self, num: int) -> list[Item]:
        return [self.create_item(i) for i in range(num)]

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def create_item(self, index: int) -> Item:
        assert len(self.items) > 0

        return self.items[index % len(self.items)]


class RandomItemShop(Shop):
    def create_item(self, _: int) -> Item:
        return choice(self.items)
