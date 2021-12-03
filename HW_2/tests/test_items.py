import pytest
from items import BabyFood, Car, Chacha, Collection, Item, Pack


@pytest.fixture
def car() -> Car:
    return Car()


@pytest.fixture
def chacha() -> Chacha:
    return Chacha()


@pytest.fixture
def baby_food() -> BabyFood:
    return BabyFood()


@pytest.fixture
def chacha_six_pack() -> Pack:
    return Pack(Chacha(), 6)


@pytest.fixture
def chacha_two_pack() -> Pack:
    return Pack(Chacha(), 2)


@pytest.fixture
def car_three_pack() -> Pack:
    return Pack(Car(), 3)


@pytest.fixture
def car_and_chacha() -> Collection:
    return Collection({Car(), Chacha()})


def test_single_items(car: Item, chacha: Item, baby_food: Item) -> None:
    assert car != chacha
    assert car != baby_food
    assert chacha != baby_food

    car_other = Car()
    assert car_other == car

    assert car.units == 1
    assert chacha.units == 1
    assert baby_food.units == 1

    assert car.name == "Car"
    assert chacha.name == "Chacha"
    assert baby_food.name == "Baby Food"

    assert car.price == 5000.01
    assert chacha.price == 19.99
    assert baby_food.price == 2.49


def test_packs(
    chacha_six_pack: Pack,
    chacha_two_pack: Pack,
    car_three_pack: Pack,
    chacha: Item,
    car: Item,
) -> None:
    assert chacha_six_pack.price == chacha.price
    assert chacha_six_pack.name == chacha.name
    assert chacha_six_pack.units == 6

    assert chacha_two_pack.price == chacha_six_pack.price
    assert chacha_two_pack.name == chacha_six_pack.name
    assert chacha_two_pack.units == 2

    assert car_three_pack.name == car.name
    assert car_three_pack.price == car.price
    assert car_three_pack.units == 3

    assert car_three_pack != car
    assert chacha_two_pack != chacha
    assert chacha_six_pack != chacha
    assert chacha_two_pack != chacha_six_pack

    car_three_pack_other = Pack(Car(), 3)
    assert car_three_pack == car_three_pack_other


def test_Collections(car_and_chacha: Collection, car: Item, chacha: Item) -> None:
    item_set: set[Item] = {Car(), Chacha()}
    name: str = ""
    for item in item_set:
        name += f"{item.name}-"
    name += "Collection"

    assert car_and_chacha.units == 1
    assert car_and_chacha.name == name
    assert car_and_chacha.price == car.price + chacha.price

    car_and_chacha_other = Collection({Car(), Chacha()})
    chacha_and_baby_food = Collection({Chacha(), BabyFood()})
    assert car_and_chacha == car_and_chacha_other
    assert car_and_chacha != chacha_and_baby_food
