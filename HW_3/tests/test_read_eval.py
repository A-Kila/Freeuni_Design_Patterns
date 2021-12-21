import pytest
from database import DummyDataBase
from event_manager import EventManger
from operation import Publish, Subscribe
from read_eval import ReadEval


SUB_COMMAND: str = "subscribe <user> to <channel>"
PUB_COMMAND: str = "publish video on <channel>"
INVALID_MSG: str = "Invalid command, try again.\n"


@pytest.fixture
def read_eval_no_sub() -> ReadEval:
    return ReadEval(EventManger(DummyDataBase()), [Publish()])


def test_read_eval(capsys: pytest.CaptureFixture[str]) -> None:
    read_eval: ReadEval = ReadEval(EventManger(DummyDataBase()))

    capsys.readouterr()

    read_eval.execute_command(SUB_COMMAND)
    out_re: str = capsys.readouterr().out
    Subscribe().execute(read_eval.event_manager, SUB_COMMAND)
    out_oper: str = capsys.readouterr().out

    assert out_re == out_oper

    read_eval.execute_command(PUB_COMMAND)
    out_re = capsys.readouterr().out
    Publish().execute(read_eval.event_manager, PUB_COMMAND)
    out_oper = capsys.readouterr().out

    assert out_re == out_oper

    read_eval.execute_command("Random wrong command")
    out_re = capsys.readouterr().out

    assert out_re == INVALID_MSG


def test_read_eval_no_sub(capsys: pytest.CaptureFixture[str]) -> None:
    read_eval: ReadEval = ReadEval(EventManger(DummyDataBase()), [Publish()])

    capsys.readouterr()

    read_eval.execute_command(PUB_COMMAND)
    out_re = capsys.readouterr().out
    Publish().execute(read_eval.event_manager, PUB_COMMAND)
    out_oper = capsys.readouterr().out

    assert out_re == out_oper

    read_eval.execute_command("Random wrong command")
    out_re = capsys.readouterr().out

    assert out_re == INVALID_MSG

    read_eval.execute_command(SUB_COMMAND)
    out_re = capsys.readouterr().out

    assert out_re == INVALID_MSG
