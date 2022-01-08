import pytest

from app.core.personel.cash_register import XReport
from app.infra.in_memory.report_repository import SqliteXReportRepository

DB_NAME: str = "test.db"


@pytest.fixture
def repo() -> SqliteXReportRepository:
    return SqliteXReportRepository(DB_NAME)


@pytest.fixture
def report1() -> XReport:
    return XReport({"item1": 2, "item2": 3}, 3.3, 6, "sometime")


@pytest.fixture
def report2() -> XReport:
    return XReport({"item3": 3, "item1": 7}, 32.3, 4, "other time")


def test_store_and_fetch_all(
    repo: SqliteXReportRepository, report1: XReport, report2: XReport
) -> None:
    repo.clear()

    assert len(repo.fetch_all()) == 0

    repo.store(report1)
    assert len(repo.fetch_all()) == 1

    repo.store(report1)
    assert len(repo.fetch_all()) == 1

    repo.store(report2)
    assert len(repo.fetch_all()) == 2

    result: dict[str, XReport] = {report1.date: report1, report2.date: report2}
    assert result == repo.fetch_all()

    repo.clear()


def test_fetch_one(
    repo: SqliteXReportRepository, report1: XReport, report2: XReport
) -> None:
    repo.clear()

    assert repo.fetch_one(report1.date) is None

    repo.store(report1)
    assert repo.fetch_one(report1.date) == report1

    assert repo.fetch_one(report2.date) is None

    repo.store(report2)
    assert repo.fetch_one(report2.date) == report2

    repo.clear()
