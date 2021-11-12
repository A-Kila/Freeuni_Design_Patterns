from dataclasses import dataclass, field

from attack_manager import AttackManager
from console_logger import ConsoleLogger
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
    movement: IMovement = field(default_factory=Crawl)
    evolution_manager: EvolutionManager = field(default_factory=EvolutionManager)
    attack_manager: IAttackManager = field(default_factory=AttackManager)

    def __post_init__(self) -> None:
        self.logger.log_stats(self.position, self.power, self.health, self.stamina)

    def move(self) -> None:
        movementStats: tuple[int, int] = self.movement.move(self.stamina)
        self.position += movementStats[0]
        self.stamina -= movementStats[1]

    def fight(self, other: ICreature) -> None:
        winner: ICreature = self.attack_manager.fight(self, other)
        winner.print_won_message()

    def evolve(self, maxEvolutions: int) -> None:
        self.evolution_manager.evolve(self, self.logger, maxEvolutions)

    def print_won_message(self) -> None:
        self.logger.print_win_message()
