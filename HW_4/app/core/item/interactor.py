from dataclasses import dataclass
from typing import Optional, Protocol

from app.core.item.items import Item
from app.core.item.price_calculator import TotalPriceCalculatorTemplate


@dataclass
class ItemResponse:
    name: str
    price: float
    units: int
    total_price: float


@dataclass
class OneItemRequest:
    key: str


@dataclass
class OneItemResponse:
    item: Optional[ItemResponse]


@dataclass
class KeyItemPair:
    key: str
    item: ItemResponse


@dataclass
class AllItemsResponse:
    items: list[KeyItemPair]


class IItemRepository(Protocol):
    def fetch_all(self) -> dict[str, Item]:
        pass

    def fetch_one(self, key: str) -> Optional[Item]:
        pass


@dataclass
class ItemInteractor:
    item_repository: IItemRepository
    price_calculator: TotalPriceCalculatorTemplate

    def _get_item_response(self, item: Item) -> ItemResponse:
        return ItemResponse(
            item.name, item.price, item.units, self.price_calculator.get_price(item)
        )

    def get_item(self, key: str) -> Optional[Item]:
        return self.item_repository.fetch_one(key)

    def get_one_item(self, item_request: OneItemRequest) -> OneItemResponse:
        item = self.get_item(item_request.key)

        if item is None:
            return OneItemResponse(None)

        return OneItemResponse(self._get_item_response(item))

    def get_all_items(self) -> AllItemsResponse:
        items: dict[str, Item] = self.item_repository.fetch_all()

        responses = list(
            map(
                lambda x: KeyItemPair(x[0], self._get_item_response(x[1])),
                items.items(),
            )
        )

        return AllItemsResponse(responses)
