import pytest
from _pytest.capture import CaptureResult
from consoleLogger import PreyLogger
from creature import Creature
from evolution import (
    BigClaw,
    BigTooth,
    EvolutionAdapter,
    Leg,
    MediumClaw,
    MediumTooth,
    SmallClaw,
    SmallTooth,
    Wing,
)
from interfaces import ICreature, IEvolution


@pytest.fixture
def dummyCreature() -> ICreature:
    return Creature(PreyLogger(), 0)


@pytest.fixture
def evolutionAdapter() -> EvolutionAdapter:
    return EvolutionAdapter(PreyLogger())


def test_evolution_counter(dummyCreature: ICreature) -> None:
    evolution1 = SmallTooth()
    evolution2 = SmallTooth()

    assert evolution1.numEvolve == 0
    assert evolution2.numEvolve == 0

    evolution1.evolve(dummyCreature)
    evolution1.evolve(dummyCreature)

    assert evolution1.numEvolve == 2
    assert evolution2.numEvolve == 0

    evolution2.evolve(dummyCreature)

    assert evolution1.numEvolve == 2
    assert evolution2.numEvolve == 1


def test_attack_evolution(dummyCreature: ICreature) -> None:
    smTooth: IEvolution = SmallTooth()
    midTooth: IEvolution = MediumTooth()
    bigTooth: IEvolution = BigTooth()

    smClaw: IEvolution = SmallClaw()
    midClaw: IEvolution = MediumClaw()
    bigClaw: IEvolution = BigClaw()

    smTooth.evolve(dummyCreature)
    assert dummyCreature.power == 4

    midTooth.evolve(dummyCreature)
    assert dummyCreature.power == 10

    bigTooth.evolve(dummyCreature)
    assert dummyCreature.power == 19

    smClaw.evolve(dummyCreature)
    assert dummyCreature.power == 38

    midClaw.evolve(dummyCreature)
    assert dummyCreature.power == 114

    bigClaw.evolve(dummyCreature)
    assert dummyCreature.power == 456


def test_move_evolution(dummyCreature: ICreature) -> None:
    leg: IEvolution = Leg()
    wing: IEvolution = Wing()

    dummyCreature.move()
    assert dummyCreature.position == 1
    assert dummyCreature.stamina == 99

    leg.evolve(dummyCreature)
    dummyCreature.move()
    assert dummyCreature.position == 4
    assert dummyCreature.stamina == 97

    leg.evolve(dummyCreature)
    dummyCreature.move()
    assert dummyCreature.position == 10
    assert dummyCreature.stamina == 93

    wing.evolve(dummyCreature)
    dummyCreature.move()
    assert dummyCreature.position == 16
    assert dummyCreature.stamina == 89

    wing.evolve(dummyCreature)
    dummyCreature.move()
    assert dummyCreature.position == 24
    assert dummyCreature.stamina == 85

    dummyCreature.move()
    assert dummyCreature.position == 32
    assert dummyCreature.stamina == 81

    dummyCreature.move()
    assert dummyCreature.position == 40
    assert dummyCreature.stamina == 77

    dummyCreature.move()
    assert dummyCreature.position == 46
    assert dummyCreature.stamina == 73


def test_evolution_adapter(
    capsys: pytest.CaptureFixture[str],
    evolutionAdapter: EvolutionAdapter,
    dummyCreature: ICreature,
) -> None:
    evolutions: list[IEvolution] = [SmallTooth()]
    evolutions[0].evolve(dummyCreature)
    evolutions[0].evolve(dummyCreature)

    capsys.readouterr()
    evolutionAdapter.logEvolutions(evolutions)
    captured: CaptureResult[str] = capsys.readouterr()
    assert captured.out == "Prey evolved\n\tSmallTooth - 2x\n\n"

    evolutions = [SmallTooth()]
    evolutions[0].evolve(dummyCreature)

    evolutionAdapter.logEvolutions(evolutions)
    captured = capsys.readouterr()
    assert captured.out == "Prey evolved\n\tSmallTooth - 1x\n\n"


def test_evolveManager(capsys: pytest.CaptureFixture[str]) -> None:
    seed: int = 420

    creature1: Creature = Creature(PreyLogger(), 0)
    creature2: Creature = Creature(PreyLogger(), 0)

    capsys.readouterr()

    creature2.evolutionManager.setRandomSeed(seed)
    creature1.evolve(10)
    evolve1: str = capsys.readouterr().out

    creature1.evolutionManager.setRandomSeed(seed)
    creature2.evolve(10)
    evolve2: str = capsys.readouterr().out

    assert evolve1 == evolve2
