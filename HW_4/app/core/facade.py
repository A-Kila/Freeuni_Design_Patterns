from dataclasses import dataclass

from app.core.item.interactor import (
    AllItemsResponse,
    IItemRepository,
    ItemInteractor,
    OneItemRequest,
    OneItemResponse,
)
from app.core.item.price_calculator import (
    TotalPriceCalculator,
    TotalPriceCalculatorTemplate,
)
from app.core.personel.personel import (
    Cashier,
    ReceiptResponse,
    StoreManager,
    XReportResponse,
)


@dataclass
class ShopService:
    item_interactor: ItemInteractor
    cashier: Cashier
    store_manager: StoreManager

    def get_all_items(self) -> AllItemsResponse:
        return self.item_interactor.get_all_items()

    def get_item(self, item: OneItemRequest) -> OneItemResponse:
        return self.item_interactor.get_one_item(item)

    def add_item_to_shopping_list(self, item_key: str) -> None:
        item = self.item_interactor.get_item(item_key)

        self.cashier.add_item_to_receipt(item)

    def buy_items(self) -> None:
        self.cashier.buy_items_from_receipt()

    def get_current_receipt(self) -> ReceiptResponse:
        return self.cashier.get_current_receipt()

    def get_X_report(self) -> XReportResponse:
        return self.store_manager.make_X_report()

    @classmethod
    def create(
        cls,
        repository: IItemRepository,
        price_calculator: TotalPriceCalculatorTemplate = TotalPriceCalculator(),
    ) -> "ShopService":
        return cls(
            item_interactor=ItemInteractor(repository, price_calculator),
            cashier=Cashier(TotalPriceCalculator()),
            store_manager=StoreManager(),
        )
