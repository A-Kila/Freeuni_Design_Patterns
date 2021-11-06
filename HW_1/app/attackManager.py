from interfaces import ICreature


class AttackManager:
    # returns the winner
    def fight(self, creature1: ICreature, creature2: ICreature) -> ICreature:
        while creature1.health > 0 and creature2.health > 0:
            creature2.health -= creature1.power
            if creature2.health <= 0:
                break
            creature1.health -= creature2.power

        return creature1 if creature2.health <= 0 else creature2
