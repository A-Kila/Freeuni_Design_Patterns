from typing import Protocol

from event_manager import EventManger


class IOperation(Protocol):
    def execute(self, event_manager: EventManger, command: str) -> bool:
        pass


class Subscribe:
    def __is_cust(self, string: str) -> bool:
        return string[0] == "<" and string[-1] == ">"

    def __is_executable(self, tokenized: list[str]) -> bool:
        return (
            len(tokenized) == 4
            and tokenized[0] == "subscribe"
            and self.__is_cust(tokenized[1])
            and tokenized[2] == "to"
            and self.__is_cust(tokenized[3])
        )

    def execute(self, event_manager: EventManger, command: str) -> bool:
        tokenized = command.split()

        if not self.__is_executable(tokenized):
            return False

        user: str = tokenized[1][1:-1]
        channel: str = tokenized[3][1:-1]
        event_manager.subscribe(user, channel)

        print(f"{user} subscribed to {channel}")

        return True


class Publish:
    def __is_cust(self, string: str) -> bool:
        return string[0] == "<" and string[-1] == ">"

    def __is_executable(self, tokenized: list[str]) -> bool:
        return (
            len(tokenized) == 4
            and tokenized[0] == "publish"
            and tokenized[1] == "video"
            and tokenized[2] == "on"
            and self.__is_cust(tokenized[3])
        )

    def execute(self, event_manager: EventManger, command: str) -> bool:
        tokenized = command.split()

        if not self.__is_executable(tokenized):
            return False

        channel: str = tokenized[3][1:-1]
        print(f"Notifying subscribers of {channel}")

        event_manager.notify(channel)

        return True
