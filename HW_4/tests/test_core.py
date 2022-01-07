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
from app.core.personel.personel import ReceiptResponse, XReportResponse
from app.infra.in_memory.in_memory import DummyMemory


@pytest.fixture
def item1() -> ItemResponse:
    return ItemResponse("Item1", 9.99, 1, 9.99)


@pytest.fixture
def item2() -> ItemResponse:
    return ItemResponse("Item2", 4.99, 1, 4.99)


@pytest.fixture
def item3() -> ItemResponse:
    return ItemResponse("Item3Pack", 9.99, 3, 29.97)


@pytest.fixture
def memory(
    item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> DummyMemory:
    repo = DummyMemory()

    repo.create(Item(item1.name, item1.price))
    repo.create(Item(item2.name, item2.price))
    repo.create(
        Pack(item3.name, item3.price, Item(item3.name, item3.price), item3.units)
    )

    return repo


@pytest.fixture
def core(memory: DummyMemory) -> ShopService:
    return ShopService.create(memory)


def test_get_all_items(
    core: ShopService, item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> None:
    all_items = AllItemsResponse(
        [
            KeyItemPair(item1.name, item1),
            KeyItemPair(item2.name, item2),
            KeyItemPair(item3.name, item3),
        ]
    )

    assert all_items == core.get_all_items()
    assert all_items == core.get_all_items()


def test_get_one_item(
    core: ShopService, item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> None:
    assert OneItemResponse(item1) == core.get_item(OneItemRequest(item1.name))
    assert OneItemResponse(item2) == core.get_item(OneItemRequest(item2.name))
    assert OneItemResponse(item3) == core.get_item(OneItemRequest(item3.name))
    assert OneItemResponse(None) == core.get_item(OneItemRequest("Nothing"))


def test_add_item_and_get_receipt(
    core: ShopService, item1: ItemResponse, item3: ItemResponse
) -> None:
    receipt = ReceiptResponse([], 0)

    core.add_item_to_shopping_list(item1.name)
    receipt.items.append(item1)
    receipt.sum += item1.total_price
    assert receipt == core.get_current_receipt()

    core.add_item_to_shopping_list(item3.name)
    receipt.items.append(item3)
    receipt.sum += item3.total_price
    assert receipt == core.get_current_receipt()

    core.add_item_to_shopping_list(item1.name)
    receipt.items.append(item1)
    receipt.sum += item1.total_price
    assert receipt == core.get_current_receipt()

    assert core.get_current_receipt().items[0] == item1
    assert core.get_current_receipt().items[1] == item3
    assert core.get_current_receipt().items[2] == item1


def test_buy_items_and_get_X_report(
    core: ShopService, item1: ItemResponse, item2: ItemResponse, item3: ItemResponse
) -> None:
    correct_X_report = XReportResponse({}, 0, 0)
    assert correct_X_report == core.get_X_report()

    core.add_item_to_shopping_list(item1.name)
    core.add_item_to_shopping_list(item2.name)
    core.add_item_to_shopping_list(item2.name)

    correct_X_report.items[item1.name] = 1
    correct_X_report.items[item2.name] = 2
    correct_X_report.total_revenue = item1.total_price + 2 * item2.total_price
    correct_X_report.closed_receipts += 1

    core.buy_items()
    assert correct_X_report == core.get_X_report()

    core.add_item_to_shopping_list(item3.name)
    core.add_item_to_shopping_list(item2.name)

    correct_X_report.items[item3.name] = item3.units
    correct_X_report.items[item2.name] += 1
    correct_X_report.total_revenue += item2.total_price + item3.total_price
    correct_X_report.closed_receipts += 1

    core.buy_items()
    assert correct_X_report == core.get_X_report()
