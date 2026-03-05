from models.pieces import Color, Pawn, Rook, Knight, Bishop, Queen, King
import os
from datetime import datetime
import json


class Board:

    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
        self.backup_dir = ".backups"
        self._ensure_backup_dir()
        self._setup()
        self._save_backup("initial_position")

    def _ensure_backup_dir(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _save_backup(self, label: str = None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if label:
            filename = f"{timestamp}_{label}.json"
        else:
            filename = f"{timestamp}_move_{len(self.move_history)}.json"
        
        filepath = os.path.join(self.backup_dir, filename)
        
        backup_data = {
            "timestamp": timestamp,
            "move_count": len(self.move_history),
            "move_history": self.move_history,
            "board_state": self._serialize_board()
        }
        
        with open(filepath, 'w') as f:
            json.dump(backup_data, f, indent=2)

    def _serialize_board(self) -> list:
        board_state = []
        for col in range(8):
            for row in range(8):
                piece = self.board[col][row]
                if piece:
                    board_state.append({
                        "position": [col, row],
                        "type": piece.name,
                        "color": piece.color.name,
                        "symbol": piece.symbol
                    })
        return board_state

    def _setup(self):
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
            error_msg = f"[ERROR] No piece at {from_pos}"
            print(error_msg)
            return False

        target = self.get_piece(to_pos)

        # Prevent capturing own piece
        if target is not None and target.color == piece.color:
            error_msg = f"[ERROR] Cannot capture your own piece at {to_pos}"
            print(error_msg)
            return False

        from_coord = piece.to_chess_coords(from_pos)
        to_coord = piece.to_chess_coords(to_pos)
        piece_name = f"{piece.color.name} {piece.name}"
        target_name = f"{target.color.name} {target.name}" if target else None

        success = piece.move(to_pos)

        if success:
            col_from, row_from = from_pos
            col_to, row_to = to_pos
            self.board[col_to][row_to] = piece
            self.board[col_from][row_from] = None

            move_info = {
                "move_number": len(self.move_history) + 1,
                "piece": piece_name,
                "from": from_coord,
                "to": to_coord,
                "captured": target_name if target else None
            }
            self.move_history.append(move_info)

            print(f"\nMOVE #{move_info['move_number']}")
            print(f"  {piece_name}: {from_coord} → {to_coord}")
            if target:
                target.die()
                print(f"  Captured: {target_name}")
            print()

            self._save_backup()
        else:
            print(f"Illegal move: {piece_name} {from_coord} → {to_coord}\n")

        return success

    def coords_to_position(self, chess_coord: str) -> list:
        coord = chess_coord.upper().strip()
        if len(coord) != 2:
            return None
        
        col_char = coord[0]
        row_char = coord[1]
        
        if col_char not in "ABCDEFGH" or row_char not in "12345678":
            return None
        
        col = ord(col_char) - ord('A')
        row = int(row_char) - 1
        
        return [col, row]

    def get_move_history(self) -> str:
        """Return formatted move history."""
        if not self.move_history:
            return "No moves yet."
        
        lines = ["MOVE HISTORY:", "─" * 50]
        for move in self.move_history:
            move_str = f"{move['move_number']:2d}. {move['piece']:20s} {move['from']} → {move['to']}"
            if move['captured']:
                move_str += f" (captured {move['captured']})"
            lines.append(move_str)
        return "\n".join(lines)


