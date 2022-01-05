from core.items import BabyFood, Car, Chacha, Collection, Item, Pack
from core.price_calculator import DiscountPriceCalculator
from core.receipt import Receipt


def test_receipt() -> None:
    car: Item = Car()
    chacha_pack = Pack(Chacha(), 6)
    chacha_baby_food = Collection({BabyFood(), Car()})

    items: list[Item] = [car, chacha_pack, chacha_baby_food]
    discounts: dict[Item, float] = {Car(): 0.5, Chacha(): 0.2}
    discout_price_calc: DiscountPriceCalculator = DiscountPriceCalculator(discounts)

    receipt: Receipt = Receipt(discout_price_calc)

    for item in items:
        receipt.add_item(item)

    sum: float = car.price * 0.5 + chacha_pack.price * 6 + chacha_baby_food.price
    assert receipt.sum == sum

    receipt.add_item(Car())
    sum += car.price * 0.5

    assert receipt.sum == sum
