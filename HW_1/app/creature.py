from dataclasses import dataclass, field

from attackManager import AttackManager
from consoleLogger import ConsoleLogger
from evolution import EvolutionManager
from interfaces import IAttackManager, ICreature, IMovement
from movement import Crawl


@dataclass
class Creature:
    logger: ConsoleLogger
    position: int
    power: int = 1
    health: int = 100
    stamina: int = 100
    movement: IMovement = field(default_factory=lambda: Crawl())
    evolutionManager: EvolutionManager = field(
        default_factory=lambda: EvolutionManager()
    )
    attackManager: IAttackManager = field(default_factory=lambda: AttackManager())

    def __post_init__(self) -> None:
        self.logger.logStats(self.position, self.power, self.health, self.stamina)

    def move(self) -> None:
        movementStats: tuple[int, int] = self.movement.move(self.stamina)
        self.position += movementStats[0]
        self.stamina -= movementStats[1]

    def fight(self, other: ICreature) -> None:
        winner: ICreature = self.attackManager.fight(self, other)
        winner.printWonMessage()

    def evolve(self, maxEvolutions: int) -> None:
        self.evolutionManager.evolve(self, self.logger, maxEvolutions)

    def printWonMessage(self) -> None:
        self.logger.printWinMessage()
