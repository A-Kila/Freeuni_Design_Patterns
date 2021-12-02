from abc import ABC
from dataclasses import dataclass
from itertools import count
from typing import Optional
from random import Random


@dataclass
class Item(ABC):
    name: str
    price: float


class Receipt:
    def __init__(self) -> None:
        self._items: dict[Item, int] = dict[Item, int]()
        self.sum: float = 0

    def add_item(self, item: Item) -> None:
        self.sum += item.price
        self._items[item] += 1

    def get_items_in_receipt(self) -> dict[Item, int]:
        return self._items

    def get_receipt_as_string(self) -> str:
        recipt: str = "Name    Units    Price    Total\n"

        for item, units in self._items.items():
            recipt += f"{item.name}, {units}, {item.price}, {units * item.price}\n"

        recipt += f"Sum: {self.sum}"

        return recipt


class CashRegister:
    _instance: Optional["CashRegister"] = None
    revenue: float = 0
    items_sold: dict[Item, int] = dict[Item, int]()

    @staticmethod
    def getInstance() -> "CashRegister":
        if CashRegister._instance is None:
            CashRegister._instance = CashRegister()

        return CashRegister._instance

    def add_paid_items_from_receipt(self, receipt: Receipt) -> None:
        self.revenue += receipt.sum

        for item, amount in receipt.get_items_in_receipt().items():
            if item in self.items_sold:
                self.items_sold[item] += amount
            else:
                self.items_sold[item] = amount

    def clear_cash_register(self) -> None:
        self.revenue = 0
        self.items_sold.clear()

    def get_register_info_as_string(self) -> str:
        report: str = "Name    Sold\n"

        for item, units in self.items_sold.items():
            report += f"{item.name}, {units}\n"

        report += f"Total Revenue: {self.revenue}"

        return report


class Cashier:
    def open_recipt(self) -> None:
        self.recipt: Receipt = Receipt()

    def register_items(self, items: list[Item]) -> None:
        for item in items:
            self.recipt.add_item(item)

    def print_recipt(self) -> None:
        print(self.recipt.get_receipt_as_string())

    def get_price_sum(self) -> float:
        return self.recipt.sum

    def confirm_payment(self) -> None:
        CashRegister.getInstance().add_paid_items_from_receipt(self.recipt)

    def make_z_report(self) -> None:
        CashRegister.getInstance().clear_cash_register()


class Customer:
    def pick_items(self) -> None:
        self._picked_items: list[Item] = list[Item]()

    def get_picked_items(self) -> list[Item]:
        return self._picked_items

    def pay_for_items(self) -> None:
        rand = Random().randint(0, 1)
        if rand:
            print('Payed with cash')
        else:
            print('Payed with card')


class StoreManager:
    def make_x_report(self) -> None:
        CashRegister.getInstance().get_register_info_as_string()


if __name__ == "__main__":

    for _ in range(3):
        manager: StoreManager = StoreManager()

        for i in count(1):
            customer: Customer = Customer()
            cashier: Cashier = Cashier()

            customer.pick_items()
            cashier.open_recipt()
            cashier.register_items(customer.get_picked_items())
            cashier.print_recipt()
            customer.pay_for_items()
            cashier.confirm_payment()

            if i % 20 == 0:
                manager.make_x_report()

            if i % 100 == 0:
                cashier.make_z_report()
                break
