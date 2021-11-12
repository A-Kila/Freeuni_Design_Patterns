from abc import abstractmethod


class ConsoleLogger:
    def log_stats(self, position: int, power: int, health: int, stamina: int) -> None:
        print(
            f"\tposition: {position}\n"
            + f"\tpower: {power}\n"
            + f"\thealth: {health}\n"
            + f"\tstamina: {stamina}\n"
        )

    @abstractmethod
    def log_evolutions(self) -> None:
        pass

    @abstractmethod
    def print_win_message(self) -> None:
        pass


class PreyLogger(ConsoleLogger):
    def log_evolutions(self) -> None:
        print("Prey evolved")

    def log_stats(self, position: int, power: int, health: int, stamina: int) -> None:
        print("Prey initilized with the stats:")
        super().log_stats(position, power, health, stamina)

    def print_win_message(self) -> None:
        print("Prey ran into infinity")


class PredatorLogger(ConsoleLogger):
    def log_evolutions(self) -> None:
        print("Predator evolved")

    def log_stats(self, position: int, power: int, health: int, stamina: int) -> None:
        print("Predator initilized with the stats:")
        super().log_stats(position, power, health, stamina)

    def print_win_message(self) -> None:
        print("Some R rated things have happened")
