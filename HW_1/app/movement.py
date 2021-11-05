from dataclasses import dataclass, field

from interfaces import ICreature, IMovement


@dataclass
class MovementManager:
    creature: ICreature
    speed: int = 0
    stamina: int = 0
    staminaRequired: int = 0

    def move(self) -> tuple[int, int]:
        pass


@dataclass
class BaseMovementDecorator:
    movement: IMovement
    speed: int
    stamina: int
    staminaRequired: int
    creature: ICreature = field(init=False)

    def __post_init__(self) -> None:
        self.creature = self.movement.creature

    def move(self) -> tuple[int, int]:
        superStats: tuple[int, int] = self.movement.move()

        if self.creature.stamina < self.staminaRequired or superStats[1] > self.speed:
            return superStats

        return (self.speed, self.stamina)


@dataclass
class Crawl(BaseMovementDecorator):
    speed: int = 1
    stamina: int = 1
    staminaRequired: int = 0

    def move(self) -> tuple[int, int]:
        return (self.speed, self.stamina)


@dataclass
class Hop(BaseMovementDecorator):
    speed: int = 3
    stamina: int = 2
    staminaRequired: int = 20


@dataclass
class Walk(BaseMovementDecorator):
    speed: int = 4
    stamina: int = 2
    staminaRequired: int = 40


@dataclass
class Run(BaseMovementDecorator):
    speed: int = 6
    stamina: int = 4
    staminaRequired: int = 60


@dataclass
class Fly(BaseMovementDecorator):
    speed: int = 8
    stamina: int = 4
    staminaRequired: int = 80
