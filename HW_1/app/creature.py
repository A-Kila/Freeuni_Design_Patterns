from dataclasses import dataclass, field

from endGameMessage import consoleLogger
from interfaces import ICreature, IMovement
from movement import Crawl, MovementManager


@dataclass
class Creature:
    message: consoleLogger
    position: int
    power: int = 1
    health: int = 100
    stamina: int = 100
    movement: IMovement = field(init=False)

    def __post_init__(self) -> None:
        self.movement = Crawl(MovementManager(self))

    def move(self) -> None:
        movementStats: tuple[int, int] = self.movement.move()
        self.position += movementStats[0]
        self.stamina -= movementStats[1]

    def attack(self, other: ICreature) -> None:
        pass

    def evolve(self) -> None:
        pass

    def logStats(self) -> None:
        print(
            self.message.logStats(self.position, self.power, self.health, self.stamina)
        )

    def printWonMessage(self) -> None:
        print(self.message.getWinMessage())
