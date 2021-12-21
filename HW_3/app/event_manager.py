from dataclasses import dataclass
from typing import Protocol


class IDataBase(Protocol):
    def add_pair(self, key: str, value: str) -> None:
        pass

    def get_from_key(self, key: str) -> list[str]:
        pass


@dataclass
class EventManger:
    database: IDataBase

    def subscribe(self, user: str, channel: str) -> None:
        self.database.add_pair(channel, user)

    def notify(self, channel: str) -> list[str]:
        return self.database.get_from_key(channel)
