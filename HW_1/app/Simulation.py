from random import randrange

from creature import Creature
from endGameMessage import PredatorLogger, PreyLogger

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
            position=randrange(prey.position),
            power=randrange(10),
            health=randrange(1000),
            stamina=randrange(1000),
        )
        
        prey.evolve()
        predator.evolve()
        
        prey.logStats()
        predator.logStats()

        while True:
            if predator.position >= prey.position:
                while predator.health > 0 or prey.health > 0:
                    predator.attack(prey)
                    prey.attack(predator)

                break

            if predator.stamina == 0:
                prey.printWonMessage()
                break

            prey.move()
            predator.move()
