from dataclasses import dataclass, field
from sqlite3 import Connection, Cursor, connect
from typing import Optional

from app.core.item.items import Item, Pack


@dataclass
class DummyItemRepository:
    items: dict[str, Item] = field(default_factory=dict[str, Item])

    def create(self, item: Item) -> None:
        self.items[item.key] = item

    def fetch_all(self) -> dict[str, Item]:
        return self.items

    def fetch_one(self, key: str) -> Optional[Item]:
        if key not in self.items:
            return None

        return self.items[key]


class SqliteItemRepository:
    def __init__(self, database_name: str) -> None:
        self.db_name = f"database/{database_name}"

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS items
                (key TEXT PRIMARY KEY, name TEXT, price REAL, units INT)
            """
        )

        con.commit()
        con.close()

    def clear(self) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("DELETE FROM items")

        con.commit()
        cur.close()

    def create(self, item: Item) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT key FROM items WHERE key=?", (item.key,))
        query: list[str] = cur.fetchall()

        if len(query) == 0:
            cur.execute(
                "INSERT INTO items VALUES (?, ?, ?, ?)",
                (item.key, item.name, item.price, item.units),
            )

        con.commit()
        con.close()

    def fetch_all(self) -> dict[str, Item]:
        all_items = dict[str, Item]()

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT * FROM items")
        item_list: list[tuple[str, str, float, int]] = cur.fetchall()

        all_items.update(
            map(
                lambda item: (item[0], self.get_item(item[1], item[2], item[3])),
                item_list,
            )
        )

        con.commit()
        con.close()

        return all_items

    def fetch_one(self, key: str) -> Optional[Item]:
        item: Optional[Item] = None

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT name, price, units FROM items WHERE key=?", (key,))
        item_info: Optional[tuple[str, float, int]] = cur.fetchone()

        if item_info is not None:
            item = self.get_item(item_info[0], item_info[1], item_info[2])

        con.commit()
        con.close()

        return item

    def get_item(self, name: str, price: float, units: int) -> Item:
        if units > 1:
            return Pack(Item(name, price), units)

        return Item(name, price)
