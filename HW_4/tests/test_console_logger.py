import pytest
from console_logger import CashReportLogger, RecieptLogger
from core.items import BabyFood, Car, Chacha, Collection, Item, Pack
from core.price_calculator import DiscountPriceCalculator


def test_report_logger(capsys: pytest.CaptureFixture[str]) -> None:
    items_sold: dict[Item, int] = {
        Car(): 2,
        Chacha(): 6,
        Collection({BabyFood(), Chacha()}): 2,
    }

    capsys.readouterr()

    CashReportLogger(items_sold, 420.69).log_to_console()

    output: str = "Name    Sold\n"
    for item, units in items_sold.items():
        output += f"{item.name}    {units}\n"
    output += "Total Revenue: 420.69\n\n"

    assert capsys.readouterr().out == output


def test_receipt_logger(capsys: pytest.CaptureFixture[str]) -> None:
    items: list[Item] = [Car(), Pack(Chacha(), 4), Collection({BabyFood(), Car()})]
    discounts: dict[Item, float] = {Car(): 0.5}
    discount_price_calc: DiscountPriceCalculator = DiscountPriceCalculator(discounts)

    capsys.readouterr()

    RecieptLogger(discount_price_calc, items, 420.69).log_to_console()

    output: str = "Name    Units    Price    Total\n"
    for item in items:
        output += f"{item.name}    {item.units}    {item.price}    {discount_price_calc.get_price(item)}\n"
    output += "Sum: 420.69\n\n"

    assert capsys.readouterr().out == output
