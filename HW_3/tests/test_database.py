from sqlite3 import Connection, Cursor, connect

import pytest
from database import DummyDataBase, SqlLiteDataBase


@pytest.fixture
def dummy_db() -> DummyDataBase:
    return DummyDataBase()


@pytest.fixture
def sql_lite() -> SqlLiteDataBase:
    return SqlLiteDataBase()


def remove_from_sqllite(channel: str, user: str) -> None:
    con: Connection = connect("subscribers.db")
    cur: Cursor = con.cursor()

    cur.execute("DELETE FROM subscribers WHERE channel=? AND user=?", (channel, user))

    con.commit()
    con.close()


def test_dummy(dummy_db: DummyDataBase) -> None:
    dummy_db.add_pair("1", "1")
    dummy_db.add_pair("1", "2")
    dummy_db.add_pair("2", "3")
    dummy_db.add_pair("2", "4")
    dummy_db.add_pair("3", "1")

    assert dummy_db.get_from_key("1") == {"1", "2"}
    assert dummy_db.get_from_key("2") == {"3", "4"}
    assert dummy_db.get_from_key("3") == {"1"}

    dummy_db.add_pair("1", "3")
    dummy_db.add_pair("1", "1")

    assert dummy_db.get_from_key("1") == {"1", "2", "3"}


def test_sql_lite(sql_lite: SqlLiteDataBase) -> None:
    sql_lite.add_pair("1", "1")
    sql_lite.add_pair("1", "2")
    sql_lite.add_pair("2", "3")
    sql_lite.add_pair("2", "4")
    sql_lite.add_pair("3", "1")

    assert sql_lite.get_from_key("1") == {"1", "2"}
    assert sql_lite.get_from_key("2") == {"3", "4"}
    assert sql_lite.get_from_key("3") == {"1"}

    sql_lite.add_pair("1", "3")
    sql_lite.add_pair("1", "1")

    assert sql_lite.get_from_key("1") == {"1", "2", "3"}

    remove_from_sqllite("1", "1")
    remove_from_sqllite("1", "2")
    remove_from_sqllite("1", "3")
    remove_from_sqllite("2", "3")
    remove_from_sqllite("2", "4")
    remove_from_sqllite("3", "1")

    assert sql_lite.get_from_key("1") == set()
    assert sql_lite.get_from_key("2") == set()
    assert sql_lite.get_from_key("3") == set()
