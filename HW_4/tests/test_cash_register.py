import pytest
from cash_register import CashRegister
from items import BabyFood, Car, Chacha, Collection, Item, Pack
from price_calculator import DiscountPriceCalculator
from receipt import Receipt


@pytest.fixture
def register() -> CashRegister:
    register = CashRegister.getInstance()

    return register


def test_register(register: CashRegister) -> None:
    car: Item = Car()
    chacha_pack = Pack(Chacha(), 6)
    chacha_baby_food = Collection({BabyFood(), Car()})

    items1: list[Item] = [car, chacha_pack, chacha_baby_food]
    items2: list[Item] = [car, car, chacha_baby_food, car]
    discounts: dict[Item, float] = {Car(): 0.5, Chacha(): 0.2}
    discout_price_calc: DiscountPriceCalculator = DiscountPriceCalculator(discounts)

    receipt1: Receipt = Receipt(discout_price_calc)
    for item in items1:
        receipt1.add_item(item)

    receipt2: Receipt = Receipt(discout_price_calc)
    for item in items2:
        receipt2.add_item(item)

    register.add_paid_items_from_receipt(receipt1)
    register.add_paid_items_from_receipt(receipt2)
    revenue: float = (
        car.price * 0.5 * 4 + chacha_pack.price * 6 + chacha_baby_food.price * 2
    )

    assert register.revenue == revenue

    register.clear_cash_register()
    assert register.revenue == 0
    assert len(register.items_sold) == 0
