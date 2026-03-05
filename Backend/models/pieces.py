from abc import ABC, abstractmethod
import uuid
from enum import Enum

class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2
    
    @classmethod
    def _missing_(cls, value):
        raise ValueError(f"Invalid {cls.__name__} ID: {value}. Valid values: {[e.value for e in cls]}")
    
    
class BaseChessPiece(ABC):
    def __init__(self, color:Enum, name:str, symbol:str, position:list):      
        self.color = color
        self.name = name
        self.symbol = symbol
        self.position = position
        
        self.is_alive = True
        self.id = str(uuid.uuid4())
        
    def __str__(self):
        return f"{self.color.name} {self.name} at {self.position}"
    
    def __repr__(self):
        return f"{self.color.name} {self.name} at {self.position}"
        
    @abstractmethod
    def move(self, new_position: list) -> bool:
        """Move piece to new position"""
        pass
    
    def die(self) -> None:
        self.is_alive = False
    
    
class Pawn(BaseChessPiece):
    def __init__(self, color_id: int, position: list):
        super().__init__(color=Color(color_id), 
                         name="Pawn",
                         symbol="♟" if color_id == 1 else "♙",
                         position=position)
        
    def move(self, new_position: list) -> bool:
        """Pawn moves forward 1 square, or 2 on first move"""
        if not self.is_alive:
            return False
        
        row_diff = abs(new_position[0] - self.position[0])
        col_diff = abs(new_position[1] - self.position[1])
        
        if new_position[1] != self.position[1]:
            return False
        
        if row_diff == 1 or row_diff == 2:
            self.position = new_position
            return True
        
        return False


class Rook(BaseChessPiece):
    def __init__(self, color_id: int, position: list):
        super().__init__(color=Color(color_id),
                         name="Rook",
                         symbol="♜" if color_id == 1 else "♖",
                         position=position)
    
    def move(self, new_position: list) -> bool:
        """Rook moves horizontally or vertically"""
        if not self.is_alive:
            return False
        
        if new_position[0] == self.position[0] or new_position[1] == self.position[1]:
            self.position = new_position
            return True
        
        return False


class Knight(BaseChessPiece):
    def __init__(self, color_id: int, position: list):
        super().__init__(color=Color(color_id),
                         name="Knight",
                         symbol="♞" if color_id == 1 else "♘",
                         position=position)
    
    def move(self, new_position: list) -> bool:
        """Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular"""
        if not self.is_alive:
            return False
        
        row_diff = abs(new_position[0] - self.position[0])
        col_diff = abs(new_position[1] - self.position[1])
        
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            self.position = new_position
            return True
        
        return False


class Bishop(BaseChessPiece):
    def __init__(self, color_id: int, position: list):
        super().__init__(color=Color(color_id),
                         name="Bishop",
                         symbol="♝" if color_id == 1 else "♗",
                         position=position)
    
    def move(self, new_position: list) -> bool:
        """Bishop moves diagonally"""
        if not self.is_alive:
            return False
        
        row_diff = abs(new_position[0] - self.position[0])
        col_diff = abs(new_position[1] - self.position[1])
        
        if row_diff == col_diff and row_diff > 0:
            self.position = new_position
            return True
        
        return False


class Queen(BaseChessPiece):
    def __init__(self, color_id: int, position: list):
        super().__init__(color=Color(color_id),
                         name="Queen",
                         symbol="♛" if color_id == 1 else "♕",
                         position=position)
    
    def move(self, new_position: list) -> bool:
        """Queen moves horizontally, vertically, or diagonally"""
        if not self.is_alive:
            return False
        
        row_diff = abs(new_position[0] - self.position[0])
        col_diff = abs(new_position[1] - self.position[1])
        
        if (new_position[0] == self.position[0] or new_position[1] == self.position[1] or 
            row_diff == col_diff) and (row_diff > 0 or col_diff > 0):
            self.position = new_position
            return True
        
        return False


class King(BaseChessPiece):
    def __init__(self, color_id: int, position: list):
        super().__init__(color=Color(color_id),
                         name="King",
                         symbol="♚" if color_id == 1 else "♔",
                         position=position)
    
    def move(self, new_position: list) -> bool:
        """King moves 1 square in any direction"""
        if not self.is_alive:
            return False
        
        row_diff = abs(new_position[0] - self.position[0])
        col_diff = abs(new_position[1] - self.position[1])
        
        if row_diff <= 1 and col_diff <= 1 and (row_diff > 0 or col_diff > 0):
            self.position = new_position
            return True
        
        return False


class EmptySpace(BaseChessPiece):
    """Represents an empty square on the board"""
    def __init__(self, position: list):
        super().__init__(color=Color.NONE,
                         name="Empty",
                         symbol="·",
                         position=position)
        self.is_alive = False
    
    def move(self, new_position: list) -> bool:
        """Empty space cannot move"""
        return False

if __name__ == "__main__":
    white_pawn = Pawn(Color.WHITE.value, [1, 0])
    black_king = King(Color.BLACK.value, [7, 4])
    white_queen = Queen(Color.WHITE.value, [0, 3])
    empty = EmptySpace([3, 3])
    
    print(white_pawn)
    print(black_king)
    print(white_queen)
    print(empty)
    
    print(white_pawn.move([2, 0]))
    print(black_king.move([6, 5]))
    print(white_queen.move([0, 7]))
    print(empty.move([4, 4]))