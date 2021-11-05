from interfaces import IMovement


class Crawl:
    speed: int = 1
    stamina: int = 1
    staminaRequired: int = 0

    def move(self, staminaAvailable: int) -> tuple[int, int]:
        if staminaAvailable <= 0:
            return (0, 0)

        return (self.speed, self.stamina)


# BaseMovementDecorator chooses the fastest available option from all the used decorators
class BaseMovementDecorator:
    movement: IMovement
    speed: int
    stamina: int
    staminaRequired: int

    def __init__(self, movement: IMovement) -> None:
        self.movement = movement

    def move(self, staminaAvailable: int) -> tuple[int, int]:
        superStats: tuple[int, int] = self.movement.move(staminaAvailable)

        if staminaAvailable < self.staminaRequired or superStats[0] > self.speed:
            return superStats

        return (self.speed, self.stamina)


class HopDecorator(BaseMovementDecorator):
    speed: int = 3
    stamina: int = 2
    staminaRequired: int = 20


class WalkDecorator(BaseMovementDecorator):
    speed: int = 4
    stamina: int = 2
    staminaRequired: int = 40


class RunDecorator(BaseMovementDecorator):
    speed: int = 6
    stamina: int = 4
    staminaRequired: int = 60


class FlyDecorator(BaseMovementDecorator):
    speed: int = 8
    stamina: int = 4
    staminaRequired: int = 80
