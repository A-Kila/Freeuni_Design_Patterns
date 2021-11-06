import pytest
from consoleLogger import PredatorLogger, PreyLogger


def test_logStats(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()

    PreyLogger().logStats(1, 1, 1, 1)
    assert (
        capsys.readouterr().out
        == "Prey initilized with the stats:\n\tposition: 1\n\tpower: 1\n\thealth: 1\n\tstamina: 1\n\n"
    )

    PredatorLogger().logStats(1, 1, 1, 1)
    assert (
        capsys.readouterr().out
        == "Predator initilized with the stats:\n\tposition: 1\n\tpower: 1\n\thealth: 1\n\tstamina: 1\n\n"
    )


def test_winMessage(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()

    PreyLogger().printWinMessage()
    assert capsys.readouterr().out == "Prey ran into infinity\n"

    PredatorLogger().printWinMessage()
    assert capsys.readouterr().out == "Some R rated things have happened\n"


def test_logEvolutions(capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()

    PreyLogger().logEvolutions()
    assert capsys.readouterr().out == "Prey evolved\n"

    PredatorLogger().logEvolutions()
    assert capsys.readouterr().out == "Predator evolved\n"
