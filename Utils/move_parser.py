def parse_input(move_str):
    """Parses a move string like '3 4' and returns a tuple (3, 4)"""
    try:
        x, y = map(int, move_str.strip().split())
        return x, y
    except ValueError:
        print("Invalid input format. Please enter two integers separated by a space.")
        return None
    except Exception as e:
        print(f"Error parsing input: {e}")
        return None
