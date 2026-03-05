from models.pieces import Color, Pawn, Rook, Knight, Bishop, Queen, King

class ChessBoard:

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._setup()

    def _setup(self):
        """Place all pieces in their standard starting positions."""

        for col in range(8):
            self.board[col][1] = Pawn(Color.WHITE, [col, 1])
            self.board[col][6] = Pawn(Color.BLACK, [col, 6])

        self.board[0][0] = Rook(Color.WHITE, [0, 0])
        self.board[7][0] = Rook(Color.WHITE, [7, 0])
        self.board[0][7] = Rook(Color.BLACK, [0, 7])
        self.board[7][7] = Rook(Color.BLACK, [7, 7])

        self.board[1][0] = Knight(Color.WHITE, [1, 0])
        self.board[6][0] = Knight(Color.WHITE, [6, 0])
        self.board[1][7] = Knight(Color.BLACK, [1, 7])
        self.board[6][7] = Knight(Color.BLACK, [6, 7])

        self.board[2][0] = Bishop(Color.WHITE, [2, 0])
        self.board[5][0] = Bishop(Color.WHITE, [5, 0])
        self.board[2][7] = Bishop(Color.BLACK, [2, 7])
        self.board[5][7] = Bishop(Color.BLACK, [5, 7])

        self.board[3][0] = Queen(Color.WHITE, [3, 0])
        self.board[3][7] = Queen(Color.BLACK, [3, 7])

        self.board[4][0] = King(Color.WHITE, [4, 0])
        self.board[4][7] = King(Color.BLACK, [4, 7])

    def display(self) -> str:
        lines = []
        lines.append("   A B C D E F G H")
        for row in range(7, -1, -1):
            rank = row + 1
            row_str = f" {rank} "
            for col in range(8):
                piece = self.board[col][row]
                if piece:
                    row_str += f"{piece.symbol} "
                else:
                    row_str += "- " if (col + row) % 2 == 0 else "+ "
            lines.append(row_str)
        return "\n".join(lines)


    def get_piece(self, position) -> object:
        col, row = position
        return self.board[col][row]

    def move_piece(self, from_pos, to_pos) -> bool:
        piece = self.get_piece(from_pos)

        if piece is None:
            print(f"  [ERROR] No piece at {piece.to_chess_coords(from_pos) if piece else from_pos}")
            return False

        target = self.get_piece(to_pos)

        # Prevent capturing own piece
        if target is not None and target.color == piece.color:
            print(f"Cannot capture your own piece at {piece.to_chess_coords(to_pos)}")
            return False

        success = piece.move(to_pos)

        if success:
            # Capture
            if target is not None:
                target.die()
                print(f"{target.color.name} {target.name} captured!")

            col_from, row_from = from_pos
            col_to, row_to = to_pos
            self.board[col_to][row_to] = piece
            self.board[col_from][row_from] = None

        return success


if __name__ == "__main__":

    print("=" * 50)
    print("CHESS BOARD — FULL TEST")
    print("=" * 50)

    game = ChessBoard()

    print("\nInitial board:")
    print(game.display())

    print("─" * 50)
    print("TEST 1: White pawn E2 → E4 (double step)")
    print("─" * 50)
    game.move_piece([4, 1], [4, 3])
    print(game.display())

    print("─" * 50)
    print("TEST 2: Black pawn E7 → E5 (double step)")
    print("─" * 50)
    game.move_piece([4, 6], [4, 4])
    print(game.display())

    print("─" * 50)
    print("TEST 3: White knight B1 → C3")
    print("─" * 50)
    game.move_piece([1, 0], [2, 2])
    print(game.display())

    print("─" * 50)
    print("TEST 4: Illegal move — white pawn E4 → E6 (too far)")
    print("─" * 50)
    game.move_piece([4, 3], [4, 5])

    print("─" * 50)
    print("TEST 5: Illegal — capture own piece (white pawn → white knight)")
    print("─" * 50)
    game.move_piece([4, 3], [2, 2])

    print("─" * 50)
    print("TEST 6: White pawn D2 → D4, black pawn captures D4")
    print("─" * 50)
    game.move_piece([3, 1], [3, 3])
    game.move_piece([4, 4], [3, 3])
    print(game.display())