from dataclasses import dataclass


@dataclass
class Item:
    _name: str
    _price: float

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

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


@dataclass
class Pack(Item):
    _item: Item
    _units: int

    @property
    def name(self) -> str:
        return self._item.name

    @property
    def price(self) -> float:
        return self._item.price

    @property
    def units(self) -> int:
        return self._units

    def __hash__(self) -> int:
        return super().__hash__()


# We Do not need this class in this assignment
@dataclass
class Collection(Item):
    _items: set[Item]

    # Count property values once
    def __post_init__(self) -> None:
        assert len(self._items) > 1

        self._name: str = ""
        self._price: float = 0

        for item in self._items:
            self._name += f"{item.name}-"
            self._price += item.price

        self._name += "Collection"

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def units(self) -> int:
        return 1

    def __hash__(self) -> int:
        return super().__hash__()
