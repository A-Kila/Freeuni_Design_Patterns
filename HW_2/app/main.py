from itertools import count
from random import randint

from items import BabyFood, Car, Chacha, Collection, Item, Pack
from personel import Cashier, Customer, StoreManager
from price_calculator import DiscountPriceCalculator

if __name__ == "__main__":
    for _ in range(3):
        manager: StoreManager = StoreManager()

        for i in count(1):
            customer: Customer = Customer()
            cashier: Cashier = Cashier()

            discounts: dict[Item, float] = {
                Collection({Car(), Chacha()}): 0.7,
                BabyFood(): 0.1,
                Pack(Chacha(), 6): 0.2,
            }

            customer.pick_items(randint(1, 100))
            cashier.open_recipt(DiscountPriceCalculator(discounts))
            cashier.register_items(customer.get_picked_items())
            cashier.print_recipt()
            customer.pay_for_items()
            cashier.confirm_payment()

            if i % 20 == 0:
                manager.make_x_report()

            if i % 100 == 0:
                cashier.make_z_report()
                break
