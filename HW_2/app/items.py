from typing import Protocol


class Item(Protocol):
    @property
    def name(self) -> str:
        pass

    @property
    def price(self) -> float:
        pass

    @property
    def units(self) -> int:
        pass


class Chacha:
    @property
    def name(self) -> str:
        return "Chacha"

    @property
    def price(self) -> float:
        return 19.99

    @property
    def units(self) -> int:
        return 1


class ChachaSixPack:
    def __init__(self) -> None:
        super().__init__()
        self.chacha = Chacha()

    @property
    def name(self) -> str:
        return self.chacha.name

    @property
    def price(self) -> float:
        return self.chacha.price

    @property
    def units(self) -> int:
        return 6


class BabyFood:
    @property
    def name(self) -> str:
        return "Baby Food"

    @property
    def price(self) -> float:
        return 2.49

    @property
    def units(self) -> int:
        return 1


class Car:
    @property
    def name(self) -> str:
        return "Car"

    @property
    def price(self) -> float:
        return 5000.01

    @property
    def units(self) -> int:
        return 1


class CarBatch:
    def __init__(self) -> None:
        super().__init__()
        self.car = Car()

    @property
    def name(self) -> str:
        return self.car.name

    @property
    def price(self) -> float:
        return self.car.price

    @property
    def units(self) -> int:
        return 3


class ChachaPackCarCollection:
    def __init__(self) -> None:
        super().__init__()

        self.chacha_pack = ChachaSixPack()
        self.car = Car()

    @property
    def name(self) -> str:
        return "Chacha Six Pack and Car Bundle"

    @property
    def price(self) -> float:
        return self.car.price + self.chacha_pack.price

    @property
    def units(self) -> int:
        return 1
