import pytest
from core.items import BabyFood, Car, Chacha, Collection, Item, Pack
from core.price_calculator import (
    DiscountPriceCalculator,
    TotalPriceCalculator,
    TotalPriceCalculatorTemplate,
)


@pytest.fixture
def total_price_calc() -> TotalPriceCalculator:
    return TotalPriceCalculator()


@pytest.fixture
def discounts() -> dict[Item, float]:
    return {
        Collection({Car(), Chacha()}): 0.7,
        BabyFood(): 0.1,
        Pack(Chacha(), 6): 0.2,
    }


@pytest.fixture
def discount_price_calc(discounts: dict[Item, float]) -> DiscountPriceCalculator:
    return DiscountPriceCalculator(discounts)


def test_total_price_calc(total_price_calc: TotalPriceCalculatorTemplate) -> None:
    assert total_price_calc.get_price(Car()) == Car().price
    assert total_price_calc.get_price(BabyFood()) == BabyFood().price
    assert total_price_calc.get_price(Pack(Chacha(), 6)) == Chacha().price * 6
    assert (
        total_price_calc.get_price(Collection({Chacha(), Car()}))
        == Chacha().price + Car().price
    )


def test_discount_price_calc(
    discount_price_calc: TotalPriceCalculatorTemplate, discounts: dict[Item, float]
) -> None:

    assert discount_price_calc.get_price(Car()) == Car().price

    assert discount_price_calc.get_price(BabyFood()) == BabyFood().price * (
        1 - discounts[BabyFood()]
    )

    assert discount_price_calc.get_price(Collection({Chacha(), Car()})) == (
        Chacha().price + Car().price
    ) * (1 - discounts[Collection({Car(), Chacha()})])

    assert discount_price_calc.get_price(Pack(Chacha(), 5)) == Chacha().price * 5
