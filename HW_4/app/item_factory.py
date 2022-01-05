from dataclasses import dataclass, field
from random import choice, seed

from core.items import BabyFood, Car, Chacha, Collection, Item, Pack


@dataclass
class Shop:
    items: list[Item] = field(
        default_factory=lambda: [
            Chacha(),
            BabyFood(),
            Car(),
            Pack(Chacha(), 6),
            Pack(Car(), 3),
            Collection({Car(), Chacha()}),
        ]
    )

    def get_items(self, num: int) -> list[Item]:
        return [self.get_item(i) for i in range(num)]

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def get_item(self, index: int) -> Item:
        assert len(self.items) > 0

        return self.items[index % len(self.items)]


class RandomItemShop(Shop):
    def set_random_seed(self, randomSeed: int) -> None:
        seed(randomSeed)

    def get_item(self, _: int) -> Item:
        return choice(self.items)
