from abc import abstractmethod


class ConsoleLogger:
    def logStats(self, position: int, power: int, health: int, stamina: int) -> None:
        print(
            f"\tposition: {position}\n"
            + f"\tpower: {power}\n"
            + f"\thealth: {health}\n"
            + f"\tstamina: {stamina}\n"
        )

    @abstractmethod
    def logEvolutions(self) -> None:
        pass

    @abstractmethod
    def printWinMessage(self) -> None:
        pass


class PreyLogger(ConsoleLogger):
    def logEvolutions(self) -> None:
        print("Prey evolved")

    def logStats(self, position: int, power: int, health: int, stamina: int) -> None:
        print("Prey initilized with the stats:")
        super().logStats(position, power, health, stamina)

    def printWinMessage(self) -> None:
        print("Prey ran into infinity")


class PredatorLogger(ConsoleLogger):
    def logEvolutions(self) -> None:
        print("Predator evolved")

    def logStats(self, position: int, power: int, health: int, stamina: int) -> None:
        print("Predator initilized with the stats:")
        super().logStats(position, power, health, stamina)

    def printWinMessage(self) -> None:
        print("Some R rated things have happened")
