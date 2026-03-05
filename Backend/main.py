from services.Board import Board

def main():
    game = Board()
    
    print("\n" + "=" * 60)
    print("  CHESS GAME — INTERACTIVE TERMINAL")
    print("=" * 60)
    print("\nCommands:")
    print("  Move: <FROM> <TO>  (e.g., 'E2 E4' or 'e2 e4')")
    print("  Board: 'board' or 'b' to display current board")
    print("  History: 'history' or 'h' to see move history")
    print("  Help: 'help' to see this message")
    print("  Exit: 'exit' or 'quit' to end game")
    print("=" * 60)
    
    print("\n" + game.display())
    
    while True:
        try:
            turn_indicator = game.current_turn.name
            user_input = input(f"\n[{turn_indicator}]> Enter move (or command): ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGame ended. Backups saved to .backups/")
                break
            elif user_input.lower() in ['board', 'b']:
                print("\n" + game.display())
                continue
            elif user_input.lower() in ['history', 'h']:
                print("\n" + game.get_move_history())
                continue
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("  Move: <FROM> <TO>  (e.g., 'E2 E4')")
                print("  Board: 'board' or 'b'")
                print("  History: 'history' or 'h'")
                print("  Help: 'help'")
                print("  Exit: 'exit' or 'quit'")
                continue
            
            parts = user_input.split()
            if len(parts) != 2:
                print("[ERROR] Invalid format. Use: <FROM> <TO> (e.g., 'E2 E4')")
                continue
            
            from_coord, to_coord = parts[0].upper(), parts[1].upper()
            from_pos = game.coords_to_position(from_coord)
            to_pos = game.coords_to_position(to_coord)
            
            if from_pos is None or to_pos is None:
                print("[ERROR] Invalid chess coordinates. Use A-H for columns, 1-8 for rows.")
                continue
            
            game.move_piece(from_pos, to_pos)
            print(game.display())
        
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Backups saved to .backups/")
            break
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()