from dataclasses import dataclass, field
from random import randrange, seed

from consoleLogger import ConsoleLogger
from interfaces import ICreature, IEvolution
from movement import FlyDecorator, HopDecorator, RunDecorator, WalkDecorator


@dataclass
class BaseEvolution:
    numEvolve: int = 0

    def evolve(self, _: ICreature) -> None:
        self.numEvolve += 1


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

        if self.numEvolve == 1:
            creature.movement = HopDecorator(creature.movement)

        if self.numEvolve == 2:
            creature.movement = RunDecorator(WalkDecorator(creature.movement))


class Wing(BaseEvolution):
    def evolve(self, creature: ICreature) -> None:
        super().evolve(creature)

        if self.numEvolve == 2:
            creature.movement = FlyDecorator(creature.movement)


class EvolutionAdapter:
    logger: ConsoleLogger

    def __init__(self, logger: ConsoleLogger) -> None:
        self.logger = logger

    def logEvolutions(self, evolutions: list[IEvolution]) -> None:
        log: str = ""

        for evolution in evolutions:
            if evolution.numEvolve != 0:
                log += f"\t{evolution.__class__.__name__} - {evolution.numEvolve}x\n"

        self.logger.logEvolutions()
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

    def __getRandomEvolution(self) -> IEvolution:
        return self.__evolutions[randrange(0, len(self.__evolutions))]

    def __getRandomEvolutions(self, maxEvolutions: int) -> list[IEvolution]:
        result: list[IEvolution] = list()
        for _ in range(randrange(0, maxEvolutions)):
            result.append(self.__getRandomEvolution())

        return result

    def setRandomSeed(self, randomSeed: int) -> None:
        seed(randomSeed)

    def addEvolution(self, evolution: IEvolution) -> None:
        self.__evolutions.append(evolution)

    def evolve(self, creature: ICreature, logger: ConsoleLogger, maxEvol: int) -> None:
        for bodyPart in self.__getRandomEvolutions(maxEvol):
            bodyPart.evolve(creature)

        EvolutionAdapter(logger).logEvolutions(self.__evolutions)
