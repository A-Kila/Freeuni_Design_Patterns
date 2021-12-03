import pytest
from item_factory import RandomItemShop, Shop
from items import BabyFood, Car, Chacha, Collection, Item, Pack


@pytest.fixture
def shop() -> Shop:
    return Shop()


@pytest.fixture
def random_shop() -> RandomItemShop:
    return RandomItemShop()


@pytest.fixture
def items() -> list[Item]:
    return [
        Chacha(),
        BabyFood(),
        Car(),
        Pack(Chacha(), 6),
        Pack(Car(), 3),
        Collection({Car(), Chacha()}),
    ]


def test_shop_(shop: Shop, items: list[Item]) -> None:
    items1: list[Item] = items.copy()
    items1.extend(items[0:2])

    items2: list[Item] = items.copy()
    items2.append(Car())
    items2.extend(items[0:2])

    assert shop.get_items(len(items1)) == items1
    shop.add_item(Car())
    assert shop.get_items(len(items2)) == items2


def test_random_shop(random_shop: RandomItemShop, items: list[Item]) -> None:
    seed: int = 69
    random_shop.set_random_seed(seed)

    rand_items1: list[Item] = random_shop.get_items(len(items))
    rand_items2: list[Item] = random_shop.get_items(len(items) + 4)

    random_shop_other: RandomItemShop = RandomItemShop()
    random_shop_other.set_random_seed(seed)

    assert random_shop_other.get_items(len(items)) == rand_items1
    assert random_shop_other.get_items(len(items) + 4) == rand_items2
