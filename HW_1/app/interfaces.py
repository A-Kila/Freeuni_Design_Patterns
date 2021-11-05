from typing import Protocol


class IMovement(Protocol):
    speed: int
    stamina: int
    staminaRequired: int

    # returns pair of position change and stamina used
    def move(self, staminaAvailable: int) -> tuple[int, int]:
        pass


class ICreature(Protocol):
    power: int
    position: int
    health: int
    stamina: int
    movement: IMovement


class IEvolution(Protocol):
    numEvolve: int

    def evolve(self, creature: ICreature) -> None:
        pass
