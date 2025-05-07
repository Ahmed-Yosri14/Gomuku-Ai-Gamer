def parse_input(move_str):
    try:
        x, y = map(int, move_str.strip().split())
        return x, y
    except ValueError:
        print("Invalid input format. Please enter two integers separated by a space.")
        return None
    except Exception as e:
        print(f"Error parsing input: {e}")
        return None
