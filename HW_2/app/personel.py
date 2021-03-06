from dataclasses import dataclass, field
from random import randint

from cash_register import CashRegister
from item_factory import RandomItemShop, Shop
from items import Item
from price_calculator import DiscountPriceCalculator
from receipt import Receipt


class Cashier:
    def open_recipt(self, price_calculator: DiscountPriceCalculator) -> None:
        self.recipt: Receipt = Receipt(price_calculator)

    def register_items(self, items: list[Item]) -> None:
        for item in items:
            self.recipt.add_item(item)

    def print_recipt(self) -> None:
        self.recipt.print_receipt()

    def get_price_sum(self) -> float:
        return self.recipt.sum

    def confirm_payment(self) -> None:
        CashRegister.getInstance().add_paid_items_from_receipt(self.recipt)

    def make_z_report(self) -> bool:
        print("Do You want to make Z report? (Y/y for yes)")
        inp: str = input()

        if inp == 'y' or inp == 'Y':
            CashRegister.getInstance().clear_cash_register()

        print('')

        return inp == 'y' or inp == 'Y'


@dataclass
class Customer:
    shop: Shop = field(default_factory=RandomItemShop)

    def pick_items(self, amount: int) -> None:
        self._picked_items: list[Item] = self.shop.get_items(amount)

    def get_picked_items(self) -> list[Item]:
        return self._picked_items

    def pay_for_items(self) -> None:
        rand = randint(0, 1)

        print("Payed with cash\n") if rand else print("Payed with card\n")


class StoreManager:
    def make_x_report(self) -> None:
        print("Do You want to make X report? (Y/y for yes)")
        inp: str = input()

        if inp == 'y' or inp == 'Y':
            CashRegister.getInstance().print_register_info()

        print('')
