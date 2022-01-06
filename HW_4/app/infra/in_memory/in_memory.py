from dataclasses import dataclass, field

from app.core.item.items import Item


@dataclass
class dummyMemory:
    items: dict[str, Item] = field(default_factory=dict[str, Item])

    def create(self, item: Item) -> None:
        self.items[item.name] = item

    def fetch_all(self) -> dict[str, Item]:
        return self.items

    def fetch_one(self, key: str) -> Item:
        return self.items[key]
