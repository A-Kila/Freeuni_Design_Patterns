from dataclasses import dataclass, field
from typing import Protocol

from database import SqlLiteDataBase
from event_manager import EventManger
from operation import Publish, Subscribe


class IOperation(Protocol):
    def execute(self, event_manager: EventManger, command: str) -> bool:
        pass


@dataclass
class ReadEval:
    event_manager: EventManger = field(
        default_factory=lambda: EventManger(SqlLiteDataBase())
    )
    __operations: list[IOperation] = field(
        default_factory=lambda: [Subscribe(), Publish()]
    )

    def execute_command(self, command: str) -> None:
        for operation in self.__operations:
            if operation.execute(self.event_manager, command):
                return

        print("Invalid command, try again.")
