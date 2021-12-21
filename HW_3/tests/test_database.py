import pytest
from database import DummyDataBase, SqlLiteDataBase


@pytest.fixture
def dummy_db() -> DummyDataBase:
    return DummyDataBase()


def sql_lite() -> SqlLiteDataBase:
    return SqlLiteDataBase()


def test_dummy() -> None:
    pass
