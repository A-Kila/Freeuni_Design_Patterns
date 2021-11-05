from dataclasses import dataclass

from consoleLogger import ConsoleLogger
from evolution import EvolutionManager
from interfaces import ICreature, IMovement
from movement import Crawl


@dataclass
class Creature:
    logger: ConsoleLogger
    position: int
    power: int = 1
    health: int = 100
    stamina: int = 100
    movement: IMovement = Crawl()
    evolutionManager: EvolutionManager = EvolutionManager()

    def __post_init__(self) -> None:
        self.logger.logStats(self.position, self.power, self.health, self.stamina)

    def move(self) -> None:
        movementStats: tuple[int, int] = self.movement.move(self.stamina)
        self.position += movementStats[0]
        self.stamina -= movementStats[1]

    def attack(self, other: ICreature) -> None:
        if self.health <= 0:
            return

        other.health -= self.power
        if other.health <= 0:
            self.printWonMessage()

    def evolve(self, maxEvolutions: int) -> None:
        self.evolutionManager.evolve(self, self.logger, maxEvolutions)

    def printWonMessage(self) -> None:
        self.logger.printWinMessage()
