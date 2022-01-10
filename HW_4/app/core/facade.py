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
    AllXReportResponse,
    Cashier,
    IXReportRepository,
    Manager,
    OneXReportRequest,
    OneXReportResponse,
    ReceiptResponse,
)


@dataclass
class ShopService:
    item_interactor: ItemInteractor
    cashier: Cashier
    manager: Manager

    def get_all_items(self) -> AllItemsResponse:
        return self.item_interactor.get_all_items()

    def get_item(self, item: OneItemRequest) -> OneItemResponse:
        return self.item_interactor.get_one_item(item)

    def add_item_to_shopping_list(self, item_key: str) -> None:
        item = self.item_interactor.get_item(item_key)

        if item is not None:
            self.cashier.add_item_to_receipt(item)

    def buy_items(self) -> None:
        self.cashier.buy_items_from_receipt()

    def get_current_receipt(self) -> ReceiptResponse:
        return self.cashier.get_current_receipt()

    def get_all_X_reports(self) -> AllXReportResponse:
        return self.manager.get_all_X_reports()

    def get_one_X_report(self, date: OneXReportRequest) -> OneXReportResponse:
        return self.manager.get_one_X_report(date)

    def make_X_report(self) -> None:
        self.manager.make_X_report()

    @classmethod
    def create(
        cls,
        item_repository: IItemRepository,
        report_repository: IXReportRepository,
        price_calculator: TotalPriceCalculatorTemplate = TotalPriceCalculator(),
    ) -> "ShopService":
        return cls(
            item_interactor=ItemInteractor(item_repository, price_calculator),
            cashier=Cashier(TotalPriceCalculator()),
            manager=Manager(report_repository),
        )
