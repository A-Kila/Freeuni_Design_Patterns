from random import randrange

from consoleLogger import PredatorLogger, PreyLogger
from creature import Creature

if __name__ == "__main__":
    for _ in range(100):
        prey: Creature = Creature(
            PreyLogger(),
            position=randrange(100),
            power=randrange(10),
            health=randrange(1000),
            stamina=randrange(1000),
        )

        predator: Creature = Creature(
            PredatorLogger(),
            position=randrange(100),
            power=randrange(10),
            health=randrange(1000),
            stamina=randrange(1000),
        )

        prey.evolve(10)
        predator.evolve(10)

        while True:
            if predator.position >= prey.position:
                while predator.health > 0 and prey.health > 0:
                    predator.attack(prey)
                    prey.attack(predator)

                break

            if predator.stamina <= 0:
                prey.printWonMessage()
                break

            prey.move()
            predator.move()
