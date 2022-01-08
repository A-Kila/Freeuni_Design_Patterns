from dataclasses import dataclass, field
from sqlite3 import Connection, Cursor, connect
from typing import Optional

from app.core.personel.cash_register import XReport


@dataclass
class DummyXReportRepository:
    reports: dict[str, XReport] = field(default_factory=dict[str, XReport])

    def store(self, report: XReport) -> None:
        self.reports[report.date] = report

    def fetch_one(self, date: str) -> Optional[XReport]:
        if date not in self.reports:
            return None

        return self.reports[date]

    def fetch_all(self) -> dict[str, XReport]:
        return self.reports


class SqliteXReportRepository:
    def __init__(self, database_name: str) -> None:
        self.db_name = database_name

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS x_reports
                (date_str TEXT, revenue REAL, checks INT, item TEXT, amount INT)
            """
        )

        con.commit()
        con.close()

    def clear(self) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("DELETE FROM x_reports")

        con.commit()
        con.close()

    def store(self, report: XReport) -> None:
        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        date: str = report.date
        revenue: float = report.total_revenue
        checks_closed: int = report.closed_receipts
        items: dict[str, int] = report.items

        cur.execute("SELECT date_str FROM x_reports WHERE date_str=?", (date,))
        query: list[str] = cur.fetchall()

        if len(query) == 0:
            for item, amount in items.items():
                print(date, revenue, checks_closed, item, amount)
                cur.execute(
                    "INSERT INTO x_reports VALUES (?, ?, ?, ?, ?)",
                    (date, revenue, checks_closed, item, amount),
                )

        con.commit()
        con.close()

    def fetch_one(self, date: str) -> Optional[XReport]:
        report: Optional[XReport] = None

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute(
            "SELECT revenue, checks FROM x_reports WHERE date_str=?",
            (date,),
        )
        revenue_checks: Optional[tuple[float, int]] = cur.fetchone()

        if revenue_checks is not None:
            report = XReport({}, revenue_checks[0], revenue_checks[1], date)

            cur.execute(
                "SELECT item, amount FROM x_reports WHERE date_str=?",
                (date,),
            )

            report.items.update(cur.fetchall())

        con.commit()
        con.close()

        return report

    def fetch_all(self) -> dict[str, XReport]:
        reports = dict[str, XReport]()

        con: Connection = connect(self.db_name)
        cur: Cursor = con.cursor()

        cur.execute("SELECT date_str, revenue, checks, item, amount FROM x_reports")
        info: list[tuple[str, float, int, str, int]] = cur.fetchall()

        for date, revenue, closed_checks, item, amount in info:
            if date not in reports:
                reports[date] = XReport({}, revenue, closed_checks, date)

            reports[date].items[item] = amount

        con.commit
        con.close()

        return reports
