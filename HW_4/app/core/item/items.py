from dataclasses import dataclass


@dataclass
class Item:
    name: str
    price: float

    @property
    def key(self) -> str:
        return self.name

    @property
    def units(self) -> int:
        return 1

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False

        return (
            self.name == __o.name
            and self.units == __o.units
            and self.price == self.price
        )

    def __ne__(self, __o: object) -> bool:
        return not self == __o

    def __hash__(self) -> int:
        return hash((self.name, self.price, self.units))


class Pack(Item):
    def __init__(self, item: Item, units: int) -> None:
        super().__init__(item.name, item.price)
        self._units = units

    @property
    def key(self) -> str:
        return f"{self.name}-{self._units}Pack"

    @property
    def units(self) -> int:
        return self._units

    def __hash__(self) -> int:
        return super().__hash__()


# We Do not need this class in this assignment
class Collection(Item):
    def __init__(self, items: set[Item]) -> None:
        assert len(items) > 1

        self.name: str = ""
        self.price: float = 0

        for item in items:
            self.name += f"{item.name}-"
            self.price += item.price

        self.name += "Collection"

    def __hash__(self) -> int:
        return super().__hash__()
