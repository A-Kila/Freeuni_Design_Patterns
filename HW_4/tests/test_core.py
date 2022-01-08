import pytest

from app.core.facade import ShopService
from app.core.item.interactor import (
    AllItemsResponse,
    ItemResponse,
    KeyItemPair,
    OneItemRequest,
    OneItemResponse,
)
from app.core.item.items import Item, Pack
from app.core.personel.cash_register import CashRegister
from app.core.personel.personel import (
    AllXReportResponse,
    DateReportPair,
    OneXReportRequest,
    OneXReportResponse,
    ReceiptResponse,
    XReportResponse,
)
from app.infra.in_memory.items_repository import DummyItemRepository
from app.infra.in_memory.report_repository import DummyXReportRepository

ITEM1_KEY: str = Item("Item1", 9.99).key
ITEM2_KEY: str = Item("Item2", 4.99).key
ITEM3_KEY: str = Pack(Item("Item1", 9.99), 3).key


@pytest.fixture
def item1() -> ItemResponse:
    return ItemResponse("Item1", 9.99, 1, 9.99)


@pytest.fixture
def item2() -> ItemResponse:
    return ItemResponse("Item2", 4.99, 1, 4.99)


@pytest.fixture
def item3() -> ItemResponse:
    return ItemResponse("Item1", 9.99, 3, 29.97)


@pytest.fixture
def item_memory(
    item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> DummyItemRepository:
    repo = DummyItemRepository()

    repo.create(Item(item1.name, item1.price))
    repo.create(Item(item2.name, item2.price))
    repo.create(Pack(Item(item3.name, item3.price), item3.units))

    return repo


@pytest.fixture
def report_memory() -> DummyXReportRepository:
    return DummyXReportRepository()


@pytest.fixture
def core(
    item_memory: DummyItemRepository, report_memory: DummyXReportRepository
) -> ShopService:
    return ShopService.create(item_memory, report_memory)


def test_get_all_items(
    core: ShopService, item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> None:
    all_items = AllItemsResponse(
        [
            KeyItemPair(ITEM1_KEY, item1),
            KeyItemPair(ITEM2_KEY, item2),
            KeyItemPair(ITEM3_KEY, item3),
        ]
    )

    assert all_items == core.get_all_items()
    assert all_items == core.get_all_items()


def test_get_one_item(
    core: ShopService, item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> None:
    assert OneItemResponse(item1) == core.get_item(OneItemRequest(ITEM1_KEY))
    assert OneItemResponse(item2) == core.get_item(OneItemRequest(ITEM2_KEY))
    assert OneItemResponse(item3) == core.get_item(OneItemRequest(ITEM3_KEY))
    assert OneItemResponse(None) == core.get_item(OneItemRequest("Nothing"))


def test_add_item_and_get_receipt(
    core: ShopService, item1: ItemResponse, item3: ItemResponse
) -> None:
    receipt = ReceiptResponse([], 0)

    core.add_item_to_shopping_list(ITEM1_KEY)
    receipt.items.append(item1)
    receipt.sum += item1.total_price
    assert receipt == core.get_current_receipt()

    core.add_item_to_shopping_list(ITEM3_KEY)
    receipt.items.append(item3)
    receipt.sum += item3.total_price
    assert receipt == core.get_current_receipt()

    core.add_item_to_shopping_list(ITEM1_KEY)
    receipt.items.append(item1)
    receipt.sum += item1.total_price
    assert receipt == core.get_current_receipt()

    assert core.get_current_receipt().items[0] == item1
    assert core.get_current_receipt().items[1] == item3
    assert core.get_current_receipt().items[2] == item1


def test_buy_items_and_make_X_report_and_get_one_X_report(
    core: ShopService, item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> None:
    correct_X_report = OneXReportResponse(None)
    first_date: str = CashRegister().getInstance().date.get_date_str()
    assert correct_X_report == core.get_one_X_report(OneXReportRequest(first_date))

    core.add_item_to_shopping_list(ITEM1_KEY)
    core.add_item_to_shopping_list(ITEM2_KEY)
    core.add_item_to_shopping_list(ITEM2_KEY)

    correct_X_report.X_report = XReportResponse(
        {item1.name: 1, item2.name: 2}, item1.total_price + 2 * item2.total_price, 1
    )

    core.buy_items()
    core.make_X_report()
    assert correct_X_report == core.get_one_X_report(OneXReportRequest(first_date))

    core.add_item_to_shopping_list(ITEM3_KEY)
    core.add_item_to_shopping_list(ITEM2_KEY)

    core.buy_items()

    core.add_item_to_shopping_list(ITEM1_KEY)
    core.add_item_to_shopping_list(ITEM1_KEY)

    core.buy_items()

    assert correct_X_report == core.get_one_X_report(OneXReportRequest(first_date))

    correct_X_report.X_report.items[item3.name] = item3.units
    correct_X_report.X_report.items[item2.name] = 1
    correct_X_report.X_report.total_revenue = item2.total_price + item3.total_price
    correct_X_report.X_report.closed_receipts = 1

    correct_X_report.X_report.items[item1.name] = 2
    correct_X_report.X_report.total_revenue += 2 * item1.total_price
    correct_X_report.X_report.closed_receipts += 1

    second_date: str = CashRegister().getInstance().date.get_date_str()
    core.make_X_report()
    assert correct_X_report == core.get_one_X_report(OneXReportRequest(second_date))


def test_get_all_reports(
    core: ShopService, item1: ItemResponse, item2: ItemResponse
) -> None:
    assert AllXReportResponse([]) == core.get_all_X_reports()

    core.add_item_to_shopping_list(ITEM1_KEY)
    core.add_item_to_shopping_list(ITEM1_KEY)
    core.add_item_to_shopping_list(ITEM2_KEY)
    core.buy_items()

    report1 = XReportResponse(
        {item1.name: 2, item2.name: 1},
        2 * item1.total_price + item2.total_price,
        1,
    )
    first_date: str = CashRegister().getInstance().date.get_date_str()
    core.make_X_report()

    core.add_item_to_shopping_list(ITEM2_KEY)
    core.add_item_to_shopping_list(ITEM2_KEY)
    core.add_item_to_shopping_list(ITEM2_KEY)
    core.buy_items()

    report2 = XReportResponse({item2.name: 3}, 3 * item2.total_price, 1)
    second_date: str = CashRegister().getInstance().date.get_date_str()
    core.make_X_report()

    reports = AllXReportResponse(
        [DateReportPair(first_date, report1), DateReportPair(second_date, report2)]
    )
    assert reports == core.get_all_X_reports()
