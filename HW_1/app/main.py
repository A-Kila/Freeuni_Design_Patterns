from random import randrange

from console_logger import PredatorLogger, PreyLogger
from creature import Creature

if __name__ == "__main__":
    for i in range(100):
        print(f"---- {i} -----------------------------")
        prey: Creature = Creature(
            PreyLogger(),
            position=randrange(1, 100),
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

        prey.evolve(10)
        predator.evolve(10)

        while True:
            if predator.position >= prey.position:
                predator.fight(prey)
                break

            if predator.stamina <= 0:
                prey.print_won_message()
                break

            prey.move()
            predator.move()
