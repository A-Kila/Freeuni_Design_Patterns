import pytest
from _pytest.capture import CaptureResult
from console_logger import PreyLogger
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
def dummy_creature() -> ICreature:
    return Creature(PreyLogger(), 0)


@pytest.fixture
def evolution_adapter() -> EvolutionAdapter:
    return EvolutionAdapter(PreyLogger())


def test_evolution_counter(dummy_creature: ICreature) -> None:
    evolution_1 = SmallTooth()
    evolution_2 = SmallTooth()

    assert evolution_1.num_evolve == 0
    assert evolution_2.num_evolve == 0

    evolution_1.evolve(dummy_creature)
    evolution_1.evolve(dummy_creature)

    assert evolution_1.num_evolve == 2
    assert evolution_2.num_evolve == 0

    evolution_2.evolve(dummy_creature)

    assert evolution_1.num_evolve == 2
    assert evolution_2.num_evolve == 1


def test_attack_evolution(dummy_creature: ICreature) -> None:
    sm_tooth: IEvolution = SmallTooth()
    mid_tooth: IEvolution = MediumTooth()
    big_tooth: IEvolution = BigTooth()

    sm_claw: IEvolution = SmallClaw()
    mid_claw: IEvolution = MediumClaw()
    big_claw: IEvolution = BigClaw()

    sm_tooth.evolve(dummy_creature)
    assert dummy_creature.power == 4

    mid_tooth.evolve(dummy_creature)
    assert dummy_creature.power == 10

    big_tooth.evolve(dummy_creature)
    assert dummy_creature.power == 19

    sm_claw.evolve(dummy_creature)
    assert dummy_creature.power == 38

    mid_claw.evolve(dummy_creature)
    assert dummy_creature.power == 114

    big_claw.evolve(dummy_creature)
    assert dummy_creature.power == 456


def test_move_evolution(dummy_creature: ICreature) -> None:
    leg: IEvolution = Leg()
    wing: IEvolution = Wing()

    dummy_creature.move()
    assert dummy_creature.position == 1
    assert dummy_creature.stamina == 99

    leg.evolve(dummy_creature)
    dummy_creature.move()
    assert dummy_creature.position == 4
    assert dummy_creature.stamina == 97

    leg.evolve(dummy_creature)
    dummy_creature.move()
    assert dummy_creature.position == 10
    assert dummy_creature.stamina == 93

    wing.evolve(dummy_creature)
    dummy_creature.move()
    assert dummy_creature.position == 16
    assert dummy_creature.stamina == 89

    wing.evolve(dummy_creature)
    dummy_creature.move()
    assert dummy_creature.position == 24
    assert dummy_creature.stamina == 85

    dummy_creature.move()
    assert dummy_creature.position == 32
    assert dummy_creature.stamina == 81

    dummy_creature.move()
    assert dummy_creature.position == 40
    assert dummy_creature.stamina == 77

    dummy_creature.move()
    assert dummy_creature.position == 46
    assert dummy_creature.stamina == 73


def test_evolution_adapter(
    capsys: pytest.CaptureFixture[str],
    evolution_adapter: EvolutionAdapter,
    dummy_creature: ICreature,
) -> None:
    evolutions: list[IEvolution] = [SmallTooth()]
    evolutions[0].evolve(dummy_creature)
    evolutions[0].evolve(dummy_creature)

    capsys.readouterr()
    evolution_adapter.log_evolutions(evolutions)
    captured: CaptureResult[str] = capsys.readouterr()
    assert captured.out == "Prey evolved\n\tSmallTooth - 2x\n\n"

    evolutions = [SmallTooth()]
    evolutions[0].evolve(dummy_creature)

    evolution_adapter.log_evolutions(evolutions)
    captured = capsys.readouterr()
    assert captured.out == "Prey evolved\n\tSmallTooth - 1x\n\n"


def test_evolveManager(capsys: pytest.CaptureFixture[str]) -> None:
    seed: int = 420

    creature_1: Creature = Creature(PreyLogger(), 0)
    creature_2: Creature = Creature(PreyLogger(), 0)

    capsys.readouterr()

    creature_2.evolution_manager.set_random_seed(seed)
    creature_1.evolve(10)
    evolve_1: str = capsys.readouterr().out

    creature_1.evolution_manager.set_random_seed(seed)
    creature_2.evolve(10)
    evolve_2: str = capsys.readouterr().out

    assert evolve_1 == evolve_2
