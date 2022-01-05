from itertools import count
from random import randint

from core.items import BabyFood, Car, Chacha, Collection, Item, Pack
from core.price_calculator import DiscountPriceCalculator
from personel import Cashier, Customer, StoreManager

if __name__ == "__main__":
    for i in range(3):
        print(f"________________________{i}_________________________")
        manager: StoreManager = StoreManager()

        for j in count(1):
            print(f"~~~~~~~~~~~~~~~~~~~~{j}~~~~~~~~~~~~~~~~~~~~~~")
            customer: Customer = Customer()
            cashier: Cashier = Cashier()

            discounts: dict[Item, float] = {
                Collection({Car(), Chacha()}): 0.7,
                BabyFood(): 0.1,
                Pack(Chacha(), 6): 0.2,
            }

            customer.pick_items(randint(1, 10))
            cashier.open_recipt(DiscountPriceCalculator(discounts))
            cashier.register_items(customer.get_picked_items())
            cashier.print_recipt()
            customer.pay_for_items()
            cashier.confirm_payment()

            if j % 20 == 0:
                manager.make_x_report()

            if j % 100 == 0:
                if cashier.make_z_report():
                    break
