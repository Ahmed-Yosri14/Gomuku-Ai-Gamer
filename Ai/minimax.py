class MiniMax:
    def __init__(self, playerOne: str = 'X', playerTwo: str = 'O', maxDepth: int = 5):
        self.playerOne = playerOne  # Maximizing player
        self.playerTwo = playerTwo  # Minimizing player
        self.maxDepth = maxDepth

        # Pattern weights for evaluation
        self.pattern_weights = {
            # Live patterns (open on both ends)
            "LIVE_TWO": 10,
            "LIVE_THREE": 100,
            "LIVE_FOUR": 1000,
            # Dead patterns (blocked on one end)
            "DEAD_TWO": 5,
            "DEAD_THREE": 25,
            "DEAD_FOUR": 100,
            # Win
            "FIVE": 100000
        }

    def is_game_over(self, board):
        """Check if the game is over (win or draw)"""
        # Check for a winner
        winner = board.hasWinner()
        if winner:
            return winner  # Return the winning player

        # Check if the board is full (draw)
        if board.isFull():
            return "Draw"

        return None  # Game is not over

    def FindBestMove(self, board, player):
        """Find the best move for the given player"""
        best_move = None
        best_score = float('-inf') if player == self.playerOne else float('inf')

        for move in self.get_relevant_moves(board):
            x, y = move
            if player == self.playerOne:
                # Maximizing player
                board[x][y] = player
                score = self.minimax(board, self.maxDepth - 1, False)
                board[x][y] = '.'
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                # Minimizing player
                board[x][y] = player
                score = self.minimax(board, self.maxDepth - 1, True)
                board[x][y] = '.'
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def get_relevant_moves(self, board):
        """Get moves that are adjacent to existing pieces (plus a small buffer)"""
        if board.isEmpty():
            # First move should be near the center for Gomoku
            center = board.l // 2
            return [(center, center)]

        relevant_moves = set()
        buffer = 2  # Consider cells within 2 spaces of existing pieces

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] != '.':  # If cell is occupied
                    # Add nearby empty cells to relevant moves
                    for di in range(-buffer, buffer + 1):
                        for dj in range(-buffer, buffer + 1):
                            ni, nj = i + di, j + dj
                            if (0 <= ni < board.l and 0 <= nj < board.l and
                                    board.grid[ni][nj] == '.'):
                                relevant_moves.add((ni, nj))

        return list(relevant_moves) if relevant_moves else board.possibleMoves()

    def minimax(self, board, depth, is_maximizing):
        # Check terminal conditions
        game_status = self.is_game_over(board)

        if game_status == self.playerOne:
            return 10000 + depth  # Win for maximizing player (higher score for quicker wins)
        elif game_status == self.playerTwo:
            return -10000 - depth  # Win for minimizing player (lower score for quicker losses)
        elif game_status == "Draw":
            return 0  # Draw

        if depth == 0:
            return self.evaluate_board(board)

        moves = self.get_relevant_moves(board)

        if is_maximizing:
            max_eval = float('-inf')
            for move in moves:
                x, y = move
                board.playMove(x, y, self.playerOne)
                eval_score = self.minimax(board, depth - 1, False)
                board.grid[x][y] = '.'
                max_eval = max(max_eval, eval_score)

            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                x, y = move
                board.playMove(x, y, self.playerTwo)
                eval_score = self.minimax(board, depth - 1, True)
                board.grid[x][y] = '.'
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

            return min_eval

    def evaluate_board(self, board):
        """Evaluate the current board position"""
        score = 0

        # Check all directions: horizontal, vertical, diagonal
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Evaluate patterns for both players
        score += self.evaluate_patterns_for_player(board, self.playerOne, directions)
        score -= self.evaluate_patterns_for_player(board, self.playerTwo, directions)

        return score

    def evaluate_patterns_for_player(self, board, player, directions):
        """Evaluate board patterns for the specified player"""
        score = 0

        # For each position on the board
        for i in range(board.l):
            for j in range(board.l):
                # For each direction
                for dx, dy in directions:
                    pattern_info = self.detect_pattern(board, i, j, dx, dy, player)
                    if pattern_info:
                        pattern_type, count = pattern_info
                        score += self.pattern_weights.get(pattern_type, 0)

        return score

    def detect_pattern(self, board, start_x, start_y, dx, dy, player):
        """
        Detect patterns starting at (start_x, start_y) in direction (dx, dy)
        Returns pattern type and count if a pattern is found
        """
        if board.grid[start_x][start_y] != player:
            return None

        # Count consecutive pieces
        count = 0
        x, y = start_x, start_y

        while (0 <= x < board.l and 0 <= y < board.l and
               board.grid[x][y] == player):
            count += 1
            x += dx
            y += dy

        if count < 2:  # Need at least 2 in a row to be interesting
            return None

        # Check if this is the start of the pattern (no player piece before it)
        is_start = (start_x - dx < 0 or start_y - dy < 0 or
                    start_x - dx >= board.l or start_y - dy >= board.l or
                    board.grid[start_x - dx][start_y - dy] != player)

        if not is_start:
            return None  # This is part of a pattern we've already counted

        # Check openness at both ends
        open_start = (0 <= start_x - dx < board.l and
                      0 <= start_y - dy < board.l and
                      board.grid[start_x - dx][start_y - dy] == '.')

        open_end = (0 <= x < board.l and
                    0 <= y < board.l and
                    board.grid[x][y] == '.')

        # Determine pattern type
        if count >= 5:
            return "FIVE", count
        elif count == 4:
            if open_start and open_end:
                return "LIVE_FOUR", count
            elif open_start or open_end:
                return "DEAD_FOUR", count
        elif count == 3:
            if open_start and open_end:
                return "LIVE_THREE", count
            elif open_start or open_end:
                return "DEAD_THREE", count
        elif count == 2:
            if open_start and open_end:
                return "LIVE_TWO", count
            elif open_start or open_end:
                return "DEAD_TWO", count
        return None

