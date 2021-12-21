from dataclasses import dataclass, field
from sqlite3 import connect, Connection, Cursor


@dataclass
class DummyDataBase:
    __map: dict[str, set[str]] = field(default_factory=lambda: {})

    def add_pair(self, key: str, value: str) -> None:
        if key not in self.__map:
            self.__map[key] = set()

        self.__map[key].add(value)

    def get_from_key(self, key: str) -> list[str]:
        if key not in self.__map:
            self.__map[key] = set() 

        return list(self.__map[key])


class SqlLiteDataBase:
    def __init__(self) -> None:
        self.db_name: str = "subscribers.db"

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS subscribers
                (channel text, user text)
        ''')

        con.commit()
        con.close()

    def add_pair(self, key: str, value: str) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()
        
        cur.execute("SELECT channel, user FROM subscribers WHERE channel=? AND user=?", (key, value))
        query: list[tuple[str, str]] = cur.fetchall()

        if len(query) == 0:
            cur.execute("INSERT INTO subscribers VALUES (?, ?)", (key, value))

        con.commit()
        con.close()

    def get_from_key(self, key: str) -> list[str]:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT user FROM subscribers WHERE channel=?", (key,))
        query: list[tuple[str]] = cur.fetchall()
        res: list[str] = list(map(lambda x: x[0], query))

        con.close()
        return res
