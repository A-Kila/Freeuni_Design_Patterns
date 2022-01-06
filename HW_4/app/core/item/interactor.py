from dataclasses import dataclass
from typing import Protocol

from app.core.item.items import Item
from app.core.item.price_calculator import TotalPriceCalculatorTemplate


@dataclass
class OneItemRequest:
    key: str


@dataclass
class OneItemResponse:
    name: str
    price: float
    units: int
    total_price: float


@dataclass
class AllItemsResponse:
    items: list[tuple[str, OneItemResponse]]


class IItemRepository(Protocol):
    def fetch_all(self) -> dict[str, Item]:
        pass

    def fetch_one(self, key: str) -> Item:
        pass


@dataclass
class ItemInteractor:
    item_repository: IItemRepository
    price_calculator: TotalPriceCalculatorTemplate

    def _get_one_item_response(self, item: Item) -> OneItemResponse:
        print(item)
        return OneItemResponse(
            item.name, item.price, item.units, self.price_calculator.get_price(item)
        )

    def get_item(self, key: str) -> Item:
        return self.item_repository.fetch_one(key)

    def get_one_item(self, item_request: OneItemRequest) -> OneItemResponse:
        item = self.get_item(item_request.key)

        return self._get_one_item_response(item)

    def get_all_items(self) -> AllItemsResponse:
        items: dict[str, Item] = self.item_repository.fetch_all()

        responses = list(
            map(lambda x: (x[0], self._get_one_item_response(x[1])), items.items())
        )

        return AllItemsResponse(responses)
