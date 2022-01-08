import pytest

from app.core.item.items import Item, Pack
from app.infra.in_memory.items_repository import SqliteItemRepository

DB_NAME = "test.db"


@pytest.fixture
def repo() -> SqliteItemRepository:
    return SqliteItemRepository(DB_NAME)


@pytest.fixture
def item1() -> Item:
    return Item("item1", 9.99)


@pytest.fixture
def item2(item1: Item) -> Item:
    return Pack(item1, 3)


def test_create_and_fetch_all(
    repo: SqliteItemRepository, item1: Item, item2: Item
) -> None:
    repo.clear()

    assert len(repo.fetch_all()) == 0

    repo.create(item1)
    assert len(repo.fetch_all()) == 1

    repo.create(item2)
    assert len(repo.fetch_all()) == 2

    repo.create(item1)
    assert len(repo.fetch_all()) == 2

    all_items: dict[str, Item] = {item1.key: item1, item2.key: item2}
    assert all_items == repo.fetch_all()

    repo.clear()


def test_fetch_one(repo: SqliteItemRepository, item1: Item, item2: Item) -> None:
    repo.clear()

    repo.create(item1)

    assert item1 == repo.fetch_one(item1.key)
    assert repo.fetch_one(item2.key) is None

    repo.create(item2)

    assert item2 == repo.fetch_one(item2.key)

    repo.clear()
