from typing import Protocol


class ICreature(Protocol):
    power: int
    position: int
    health: int
    stamina: int


class IMovement(Protocol):
    creature: ICreature
    speed: int
    stamina: int
    staminaRequired: int

    # returns pair of position change and stamina used
    def move(self) -> tuple[int, int]:
        pass
