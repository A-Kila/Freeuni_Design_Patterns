import pytest
from database import DummyDataBase
from event_manager import EventManger


def test_event_manager(capsys: pytest.CaptureFixture[str]) -> None:
    event_man: EventManger = EventManger(DummyDataBase())

    event_man.subscribe("1", "1")
    event_man.subscribe("1", "2")
    event_man.subscribe("1", "1")
    event_man.subscribe("2", "1")

    res_values: list[str] = list({"1", "2"})
    out1: str = f"\t{res_values[0]}\n\t{res_values[1]}\n"
    out2: str = "\t1\n"

    capsys.readouterr()

    event_man.notify("1")
    assert capsys.readouterr().out == out1

    event_man.notify("2")
    assert capsys.readouterr().out == out2
