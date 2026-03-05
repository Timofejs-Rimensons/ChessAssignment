from abc import ABC, abstractmethod
import uuid
from enum import Enum


class Color(Enum):
    NONE  = 0
    WHITE = 1
    BLACK = 2

    @classmethod
    def _missing_(cls, value):
        raise ValueError(f"Invalid {cls.__name__} ID: {value}. Valid values: {[e.value for e in cls]}")

class BaseChessPiece(ABC):

    COLUMNS = ["A", "B", "C", "D", "E", "F", "G", "H"]

    def __init__(self, color: Enum, name: str, symbol: str, position: list):
        self.color    = color
        self.name     = name
        self.symbol   = symbol
        self.position = position
        self.is_alive = True
        self.id       = str(uuid.uuid4())

    def __str__(self):
        return f"{self.color.name} {self.name} ({self.to_chess_coords(self.position)})"

    def __repr__(self):
        return f"{self.color.name} {self.name} ({self.to_chess_coords(self.position)})"

    def to_chess_coords(self, position) -> str:
        col, row = position
        return f"{self.COLUMNS[col]}{row + 1}"

    def _log(self, new_position, note="") -> str:
        from_coord = self.to_chess_coords(self.position)
        to_coord   = self.to_chess_coords(new_position)
        suffix     = f" ({note})" if note else ""
        return f"{self.color.name} {self.name}: {from_coord} → {to_coord}{suffix}"

    @abstractmethod
    def move(self, movement: str) -> bool:
        print(movement)

    @abstractmethod
    def die(self) -> None:
        self.is_alive = False

class Pawn(BaseChessPiece):
    def __init__(self, color: Color, position: list):
        symbol = "p" if color == Color.WHITE else "P"
        super().__init__(color, "Pawn", symbol, position)
        self.has_moved = False

    def move(self, new_position, board=None) -> bool:
        col, row         = self.position
        new_col, new_row = new_position
        direction        = 1 if self.color == Color.WHITE else -1
        row_diff         = (new_row - row) * direction
        col_diff         = abs(new_col - col)

        if col_diff == 0 and row_diff == 1:
            super().move(self._log(new_position))
            self.position = new_position
            self.has_moved = True
            return True

        if col_diff == 0 and row_diff == 2 and not self.has_moved:
            super().move(self._log(new_position, "double step"))
            self.position = new_position
            self.has_moved = True
            return True

        if col_diff == 1 and row_diff == 1:
            super().move(self._log(new_position, "capture"))
            self.position = new_position
            self.has_moved = True
            return True

        super().move(self._log(new_position, "illegal move"))
        return False

    def die(self) -> None:
        self.is_alive = False
        self.position = None

class Rook(BaseChessPiece):
    def __init__(self, color: Color, position: list):
        symbol = "r" if color == Color.WHITE else "R"
        super().__init__(color, "Rook", symbol, position)
        self.has_moved = False

    def move(self, new_position, board=None) -> bool:
        col, row         = self.position
        new_col, new_row = new_position

        if col == new_col or row == new_row:
            super().move(self._log(new_position))
            self.position = new_position
            self.has_moved = True
            return True

        super().move(self._log(new_position, "illegal move"))
        return False

    def die(self) -> None:
        self.is_alive = False
        self.position = None

class Knight(BaseChessPiece):
    def __init__(self, color: Color, position: list):
        symbol = "k" if color == Color.WHITE else "K"
        super().__init__(color, "Knight", symbol, position)

    def move(self, new_position, board=None) -> bool:
        col, row         = self.position
        new_col, new_row = new_position
        col_diff         = abs(new_col - col)
        row_diff         = abs(new_row - row)

        if sorted([col_diff, row_diff]) == [1, 2]:
            super().move(self._log(new_position))
            self.position = new_position
            return True

        super().move(self._log(new_position, "illegal move"))
        return False

    def die(self) -> None:
        self.is_alive = False
        self.position = None

class Bishop(BaseChessPiece):
    def __init__(self, color: Color, position: list):
        symbol = "b" if color == Color.WHITE else "B"
        super().__init__(color, "Bishop", symbol, position)

    def move(self, new_position, board=None) -> bool:
        col, row         = self.position
        new_col, new_row = new_position
        col_diff         = abs(new_col - col)
        row_diff         = abs(new_row - row)

        if col_diff == row_diff and col_diff != 0:
            super().move(self._log(new_position))
            self.position = new_position
            return True

        super().move(self._log(new_position, "illegal move"))
        return False

    def die(self) -> None:
        self.is_alive = False
        self.position = None

class Queen(BaseChessPiece):
    def __init__(self, color: Color, position: list):
        symbol = "q" if color == Color.WHITE else "Q"
        super().__init__(color, "Queen", symbol, position)

    def move(self, new_position, board=None) -> bool:
        col, row         = self.position
        new_col, new_row = new_position
        col_diff         = abs(new_col - col)
        row_diff         = abs(new_row - row)

        is_straight  = (col == new_col or row == new_row)
        is_diagonal  = (col_diff == row_diff and col_diff != 0)

        if is_straight or is_diagonal:
            super().move(self._log(new_position))
            self.position = new_position
            return True

        super().move(self._log(new_position, "illegal move"))
        return False

    def die(self) -> None:
        self.is_alive = False
        self.position = None

class King(BaseChessPiece):
    def __init__(self, color: Color, position: list):
        symbol = "k" if color == Color.WHITE else "K"
        super().__init__(color, "King", symbol, position)
        self.has_moved = False

    def move(self, new_position, board=None) -> bool:
        col, row         = self.position
        new_col, new_row = new_position
        col_diff         = abs(new_col - col)
        row_diff         = abs(new_row - row)

        if max(col_diff, row_diff) == 1:
            super().move(self._log(new_position))
            self.position = new_position
            self.has_moved = True
            return True

        super().move(self._log(new_position, "illegal move"))
        return False

    def die(self) -> None:
        self.is_alive = False
        self.position = None

if __name__ == "__main__":

    print("=" * 50)
    print("PAWN")
    print("=" * 50)
    p = Pawn(Color.WHITE, [4, 1])
    p.move([4, 2])
    p2 = Pawn(Color.WHITE, [3, 1])
    p2.move([3, 3])
    p2.move([3, 4])
    p2.move([3, 6])
    p2.move([4, 5])
    pb = Pawn(Color.BLACK, [0, 6])
    pb.move([0, 5])

    print("\n" + "=" * 50)
    print("ROOK")
    print("=" * 50)
    r = Rook(Color.WHITE, [0, 0])
    r.move([0, 5])
    r.move([4, 5])
    r.move([6, 7])

    print("\n" + "=" * 50)
    print("KNIGHT")
    print("=" * 50)
    n = Knight(Color.BLACK, [1, 0])
    n.move([2, 2])
    n.move([4, 3])
    n.move([5, 5])

    print("\n" + "=" * 50)
    print("BISHOP")
    print("=" * 50)
    b = Bishop(Color.WHITE, [2, 0])
    b.move([5, 3])
    b.move([7, 5])
    b.move([7, 6])

    print("\n" + "=" * 50)
    print("QUEEN")
    print("=" * 50)
    q = Queen(Color.WHITE, [3, 0])
    q.move([3, 5])
    q.move([6, 5])
    q.move([4, 4])
    q.move([6, 2])
    q.move([5, 0])

    print("\n" + "=" * 50)
    print("KING")
    print("=" * 50)
    k = King(Color.BLACK, [4, 7])
    k.move([4, 6])
    k.move([3, 5])
    k.move([3, 3])

    print("\n" + "=" * 50)
    print("DIE")
    print("=" * 50)
    victim = Pawn(Color.BLACK, [4, 4])
    print(f"Before: {victim} | alive={victim.is_alive}")
    victim.die()
    print(f"After:  alive={victim.is_alive} | position={victim.position}")
