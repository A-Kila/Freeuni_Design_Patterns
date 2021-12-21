from dataclasses import dataclass
from typing import Protocol

from notifier import PrintNotifier


class IDataBase(Protocol):
    def add_pair(self, key: str, value: str) -> None:
        pass

    def get_from_key(self, key: str) -> set[str]:
        pass


class INotifier(Protocol):
    def notify(self, user: str) -> None:
        pass


@dataclass
class EventManger:
    database: IDataBase
    notifier: INotifier = PrintNotifier()

    def subscribe(self, user: str, channel: str) -> None:
        self.database.add_pair(channel, user)

    def notify(self, channel: str) -> None:
        users: set[str] = self.database.get_from_key(channel)

        for user in users:
            self.notifier.notify(user)
