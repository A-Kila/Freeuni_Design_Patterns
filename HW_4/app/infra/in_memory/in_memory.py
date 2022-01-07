from dataclasses import dataclass, field
from typing import Optional

from app.core.item.items import Item


@dataclass
class DummyMemory:
    items: dict[str, Item] = field(default_factory=dict[str, Item])

    def create(self, item: Item) -> None:
        self.items[item.name] = item

    def fetch_all(self) -> dict[str, Item]:
        return self.items

    def fetch_one(self, key: str) -> Optional[Item]:
        if key not in self.items:
            return None

        return self.items[key]
