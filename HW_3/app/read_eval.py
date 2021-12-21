from dataclasses import dataclass, field
from enum import Enum

from data_base import SqlLiteDataBase
from event_manager import EventManger
from operation import IOperation, Publish, Subscribe


class Operation(Enum):
    SUBSCRIBE = 1
    PUBLISH = 2
    WRONG_OP = 3


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
