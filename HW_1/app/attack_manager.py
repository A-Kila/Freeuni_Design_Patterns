from interfaces import ICreature


class AttackManager:
    # returns the winner
    def fight(self, creature_1: ICreature, creature_2: ICreature) -> ICreature:
        while creature_1.health > 0 and creature_2.health > 0:
            creature_2.health -= creature_1.power
            if creature_2.health <= 0:
                break
            creature_1.health -= creature_2.power

        return creature_1 if creature_2.health <= 0 else creature_2
