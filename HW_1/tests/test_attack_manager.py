from attack_manager import AttackManager
from console_logger import PreyLogger
from creature import Creature
from interfaces import ICreature


def test_attack_manager() -> None:
    att_man: AttackManager = AttackManager()

    creature_1: ICreature = Creature(PreyLogger(), 1, 1)
    creature_2: ICreature = Creature(PreyLogger(), 1, 3)

    winner: ICreature = att_man.fight(creature_1, creature_2)

    assert winner != creature_1
    assert winner == creature_2

    creature_1 = Creature(PreyLogger(), 1, 1, 10)
    creature_2 = Creature(PreyLogger(), 1, 1, 10)

    winner = att_man.fight(creature_1, creature_2)

    assert winner == creature_1
    assert winner != creature_2
    assert winner.health == 1
