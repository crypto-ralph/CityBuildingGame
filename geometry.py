from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int

    def as_tuple(self) -> tuple:
        return self.x, self.y


@dataclass
class Size:
    width: int
    height: int

    def as_tuple(self) -> tuple:
        return self.width, self.height
