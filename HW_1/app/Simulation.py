from dataclasses import dataclass


@dataclass
class Creature:
    position: int
    power: int = 1
    health: int = 100
    stamina: int = 100
