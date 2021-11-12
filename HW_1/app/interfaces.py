from typing import Protocol


class IMovement(Protocol):
    speed: int
    stamina: int
    stamina_required: int

    # returns pair of position change and stamina used
    def move(self, stamina_available: int) -> tuple[int, int]:
        pass


class ICreature(Protocol):
    power: int
    position: int
    health: int
    stamina: int
    movement: IMovement

    def move(self) -> None:
        pass

    def print_won_message(self) -> None:
        pass


class IEvolution(Protocol):
    num_evolve: int

    def evolve(self, creature: ICreature) -> None:
        pass


class IAttackManager(Protocol):
    def fight(self, creature_1: ICreature, creature_2: ICreature) -> ICreature:
        pass
