import copy
import math
import random
from typing import List, Tuple, Optional


class MiniMax:
    def __init__(self, playerOne: str = 'X', playerTwo: str = 'O', maxDepth: int = 3):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.maxDepth = maxDepth

        # Pattern weights for evaluation
        self.pattern_weights = {
            "LIVE_TWO": 10,
            "LIVE_THREE": 100,
            "LIVE_FOUR": 1000,
            "DEAD_TWO": 1,
            "DEAD_THREE": 10,
            "DEAD_FOUR": 100,
            "FIVE": 100000
        }

    def FindBestMove(self, board, player) -> Tuple[int, int]:
        """Find the best move for the given player with fallback to random move"""
        best_move = None
        best_score = -math.inf if player == self.playerOne else math.inf

        # Get all possible moves (with optimization)
        possible_moves = self.get_relevant_moves(board)
        if not possible_moves:
            return self.get_random_move(board)

        for move in possible_moves:
            x, y = move
            if not board.validMove(x, y):
                continue

            # Make the move
            temp_board = copy.deepcopy(board)
            temp_board.playMove(x, y, player)

            # Evaluate
            if player == self.playerOne:
                score = self.minimax(temp_board, self.maxDepth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                score = self.minimax(temp_board, self.maxDepth - 1, True)
                if score < best_score:
                    best_score = score
                    best_move = move

            # Undo the move
            #board.playMove(x, y, '.')

        return best_move if best_move else self.get_random_move(board)

    def get_random_move(self, board):
        """Fallback to random valid move"""
        valid_moves = []
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    valid_moves.append((i, j))
        return random.choice(valid_moves) if valid_moves else (0, 0)

    def get_relevant_moves(self, board):
        """Get moves near existing pieces for efficiency"""
        moves = set()
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] != '.':
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if (0 <= ni < board.l and 0 <= nj < board.l and
                                    board.grid[ni][nj] == '.'):
                                moves.add((ni, nj))
        return list(moves) if moves else board.possibleMoves()

    def minimax(self, board, depth, is_maximizing):
        # Check terminal conditions
        winner = board.hasWinner()
        if winner == self.playerOne:
            return 100000 + depth
        elif winner == self.playerTwo:
            return -100000 - depth
        elif board.isFull():
            return 0

        if depth == 0:
            return self.evaluate_board(board)

        moves = self.get_relevant_moves(board)

        if is_maximizing:
            max_eval = -math.inf
            for move in moves:
                x, y = move
                temp_board = copy.deepcopy(board)
                temp_board.playMove(x, y, self.playerOne)
                eval = self.minimax(temp_board, depth - 1, False)
                board.playMove(x, y, '.')
                max_eval = max(max_eval, eval)

            return max_eval
        else:
            min_eval = math.inf
            for move in moves:
                x, y = move
                temp_board = copy.deepcopy(board)
                temp_board.playMove(x, y, self.playerOne)
                eval = self.minimax(temp_board, depth - 1, True)
                board.playMove(x, y, '.')
                min_eval = min(min_eval, eval)

            return min_eval

    def evaluate_board(self, board):
        """Improved board evaluation with pattern detection"""
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Evaluate for both players
        score += self.evaluate_player(board, self.playerOne, directions)
        score -= self.evaluate_player(board, self.playerTwo, directions)

        return score

    def evaluate_player(self, board, player, directions):
        """Evaluate board for specific player"""
        total = 0
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == player:
                    for dx, dy in directions:
                        pattern = self.detect_pattern(board, i, j, dx, dy, player)
                        if pattern:
                            total += self.pattern_weights.get(pattern, 0)
        return total

    def detect_pattern(self, board, x, y, dx, dy, player):
        """Detect and classify patterns"""
        # Check if this is the start of a pattern
        if (x - dx >= 0 and y - dy >= 0 and
                x - dx < board.l and y - dy < board.l and
                board.grid[x - dx][y - dy] == player):
            return None

        count = 0
        # Count consecutive pieces
        while (0 <= x < board.l and 0 <= y < board.l and
               board.grid[x][y] == player):
            count += 1
            x += dx
            y += dy

        if count < 2:
            return None

        # Check openness
        open_start = (x - (count + 1) * dx >= 0 and y - (count + 1) * dy >= 0 and
                      x - (count + 1) * dx < board.l and y - (count + 1) * dy < board.l and
                      board.grid[x - (count + 1) * dx][y - (count + 1) * dy] == '.')

        open_end = (0 <= x < board.l and 0 <= y < board.l and
                    board.grid[x][y] == '.')

        # Classify pattern
        if count >= 5:
            return "FIVE"
        elif count == 4:
            if open_start and open_end:
                return "LIVE_FOUR"
            elif open_start or open_end:
                return "DEAD_FOUR"
        elif count == 3:
            if open_start and open_end:
                return "LIVE_THREE"
            elif open_start or open_end:
                return "DEAD_THREE"
        elif count == 2:
            if open_start and open_end:
                return "LIVE_TWO"
            elif open_start or open_end:
                return "DEAD_TWO"
        return None
