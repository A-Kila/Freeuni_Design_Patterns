import pytest
from console_logger import PredatorLogger, PreyLogger


def test_log_stats(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()

    PreyLogger().log_stats(1, 1, 1, 1)
    assert (
        capsys.readouterr().out
        == "Prey initilized with the stats:\n\tposition: 1\n\tpower: 1\n\thealth: 1\n\tstamina: 1\n\n"
    )

    PredatorLogger().log_stats(1, 1, 1, 1)
    assert (
        capsys.readouterr().out
        == "Predator initilized with the stats:\n\tposition: 1\n\tpower: 1\n\thealth: 1\n\tstamina: 1\n\n"
    )


def test_win_message(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()

    PreyLogger().print_win_message()
    assert capsys.readouterr().out == "Prey ran into infinity\n"

    PredatorLogger().print_win_message()
    assert capsys.readouterr().out == "Some R rated things have happened\n"


def test_log_evolutions(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()

    PreyLogger().log_evolutions()
    assert capsys.readouterr().out == "Prey evolved\n"

    PredatorLogger().log_evolutions()
    assert capsys.readouterr().out == "Predator evolved\n"
