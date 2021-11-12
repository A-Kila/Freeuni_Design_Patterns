from dataclasses import dataclass, field
from random import randrange, seed

from console_logger import ConsoleLogger
from interfaces import ICreature, IEvolution
from movement import FlyDecorator, HopDecorator, RunDecorator, WalkDecorator


@dataclass
class BaseEvolution:
    num_evolve: int = 0

    def evolve(self, _: ICreature) -> None:
        self.num_evolve += 1


class Tooth(BaseEvolution):
    power: int

    def evolve(self, creature: ICreature) -> None:
        super().evolve(creature)
        creature.power += self.power


class SmallTooth(Tooth):
    power: int = 3


class MediumTooth(Tooth):
    power: int = 6


class BigTooth(Tooth):
    power: int = 9


class Claw(BaseEvolution):
    power: int

    def evolve(self, creature: ICreature) -> None:
        super().evolve(creature)
        creature.power *= self.power


class SmallClaw(Claw):
    power: int = 2


class MediumClaw(Claw):
    power: int = 3


class BigClaw(Claw):
    power: int = 4


class Leg(BaseEvolution):
    def evolve(self, creature: ICreature) -> None:
        super().evolve(creature)

        if self.num_evolve == 1:
            creature.movement = HopDecorator(creature.movement)

        if self.num_evolve == 2:
            creature.movement = RunDecorator(WalkDecorator(creature.movement))


class Wing(BaseEvolution):
    def evolve(self, creature: ICreature) -> None:
        super().evolve(creature)

        if self.num_evolve == 2:
            creature.movement = FlyDecorator(creature.movement)


class EvolutionAdapter:
    logger: ConsoleLogger

    def __init__(self, logger: ConsoleLogger) -> None:
        self.logger = logger

    def log_evolutions(self, evolutions: list[IEvolution]) -> None:
        log: str = ""

        for evolution in evolutions:
            if evolution.num_evolve != 0:
                log += f"\t{evolution.__class__.__name__} - {evolution.num_evolve}x\n"

        self.logger.log_evolutions()
        print(log)


@dataclass
class EvolutionManager:
    __evolutions: list[IEvolution] = field(
        default_factory=lambda: [
            SmallTooth(),
            MediumTooth(),
            BigTooth(),
            SmallClaw(),
            MediumClaw(),
            BigClaw(),
            Leg(),
            Wing(),
        ]
    )

    def __get_random_evolution(self) -> IEvolution:
        return self.__evolutions[randrange(0, len(self.__evolutions))]

    def __get_random_evolutions(self, max_evolutions: int) -> list[IEvolution]:
        result: list[IEvolution] = list()
        for _ in range(randrange(0, max_evolutions)):
            result.append(self.__get_random_evolution())

        return result

    def set_random_seed(self, randomSeed: int) -> None:
        seed(randomSeed)

    def add_evolution(self, evolution: IEvolution) -> None:
        self.__evolutions.append(evolution)

    def evolve(self, creature: ICreature, logger: ConsoleLogger, maxEvol: int) -> None:
        for bodyPart in self.__get_random_evolutions(maxEvol):
            bodyPart.evolve(creature)

        EvolutionAdapter(logger).log_evolutions(self.__evolutions)
