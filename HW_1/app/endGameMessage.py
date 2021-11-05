from abc import abstractmethod


class consoleLogger:
    def logStats(self, position: int, power: int, health: int, stamina: int) -> str:
        return (
            f"\tposition: {position}\n"
            + f"\tposition: {power}\n"
            + f"\tposition: {health}\n"
            + f"\tposition: {stamina}\n"
        )

    @abstractmethod
    def getWinMessage(self) -> str:
        pass


class PreyLogger(consoleLogger):
    def logStats(self, position: int, power: int, health: int, stamina: int) -> str:
        return "Prey initilized with the stats:\n" + super().logStats(
            position, power, health, stamina
        )

    def getWinMessage(self) -> str:
        return "Prey ran into infinity"


class PredatorLogger(consoleLogger):
    def logStats(self, position: int, power: int, health: int, stamina: int) -> str:
        return "Predator initilized with the stats:\n" + super().logStats(
            position, power, health, stamina
        )

    def getWinMessage(self) -> str:
        return "Some R rated things have happened"
