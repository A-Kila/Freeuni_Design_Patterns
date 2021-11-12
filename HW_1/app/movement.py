from interfaces import IMovement


class Crawl:
    speed: int = 1
    stamina: int = 1
    stamina_required: int = 0

    def move(self, stamina_available: int) -> tuple[int, int]:
        if stamina_available <= 0:
            return (0, 0)

        return (self.speed, self.stamina)


# BaseMovementDecorator chooses the fastest available option from all the used decorators
class BaseMovementDecorator:
    movement: IMovement
    speed: int
    stamina: int
    stamina_required: int

    def __init__(self, movement: IMovement) -> None:
        self.movement = movement

    def move(self, stamina_available: int) -> tuple[int, int]:
        super_stats: tuple[int, int] = self.movement.move(stamina_available)

        if stamina_available < self.stamina_required or super_stats[0] > self.speed:
            return super_stats

        return (self.speed, self.stamina)


class HopDecorator(BaseMovementDecorator):
    speed: int = 3
    stamina: int = 2
    stamina_required: int = 20


class WalkDecorator(BaseMovementDecorator):
    speed: int = 4
    stamina: int = 2
    stamina_required: int = 40


class RunDecorator(BaseMovementDecorator):
    speed: int = 6
    stamina: int = 4
    stamina_required: int = 60


class FlyDecorator(BaseMovementDecorator):
    speed: int = 8
    stamina: int = 4
    stamina_required: int = 80
