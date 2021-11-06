from attackManager import AttackManager
from consoleLogger import PreyLogger
from creature import Creature
from interfaces import ICreature


def test_attack_manager() -> None:
    attMan: AttackManager = AttackManager()

    creature1: ICreature = Creature(PreyLogger(), 1, 1)
    creature2: ICreature = Creature(PreyLogger(), 1, 3)

    winner: ICreature = attMan.fight(creature1, creature2)

    assert winner != creature1
    assert winner == creature2

    creature1 = Creature(PreyLogger(), 1, 1, 10)
    creature2 = Creature(PreyLogger(), 1, 1, 10)

    winner = attMan.fight(creature1, creature2)

    assert winner == creature1
    assert winner != creature2
    assert winner.health == 1
