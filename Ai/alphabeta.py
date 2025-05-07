import copy
import math
import random
from typing import List, Tuple, Optional


class AlphaBeta:
    def __init__(self, playerOne: str = 'X', playerTwo: str = 'O', maxDepth: int = 3):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.maxDepth = maxDepth

        # Enhanced pattern weights for evaluation
        self.pattern_weights = {
            "LIVE_TWO": 10,
            "LIVE_THREE": 100,
            "LIVE_FOUR": 10000,  # Increased weight for immediate threats
            "DEAD_TWO": 1,
            "DEAD_THREE": 10,
            "DEAD_FOUR": 100,
            "FIVE": 1000000,  # Higher weight for winning move
            "OPEN_FOUR": 100000  # Special case for immediate threat
        }

    def FindBestMove(self, board, player) -> Tuple[int, int]:
        """Find the best move for the given player with threat detection"""
        # First check for immediate winning moves or blocks
        immediate_move = self.check_immediate_moves(board, player)
        if immediate_move:
            return immediate_move

        best_move = None
        best_score = -math.inf if player == self.playerOne else math.inf

        possible_moves = self.get_relevant_moves(board)
        if not possible_moves:
            return self.get_random_move(board)

        for move in possible_moves:
            x, y = move
            if not board.validMove(x, y):
                continue

            temp_board = copy.deepcopy(board)
            temp_board.playMove(x, y, player)

            if player == self.playerOne:
                score = self.alphabeta(temp_board, self.maxDepth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                score = self.alphabeta(temp_board, self.maxDepth - 1, True)
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move if best_move else self.get_random_move(board)

    def check_immediate_moves(self, board, player):
        """Check for moves that win immediately or block opponent's win"""
        opponent = self.playerTwo if player == self.playerOne else self.playerOne

        # Check if we can win immediately
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    board.grid[i][j] = player
                    if board.hasWinner() == player:
                        board.grid[i][j] = '.'  # Undo move
                        return (i, j)
                    board.grid[i][j] = '.'  # Undo move

        # Check if we need to block opponent's open four or winning move
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    board.grid[i][j] = opponent
                    if board.hasWinner() == opponent:
                        board.grid[i][j] = '.'  # Undo move
                        return (i, j)
                    board.grid[i][j] = '.'  # Undo move

        # Check for open fours that need blocking
        open_four_moves = self.find_open_fours(board, opponent)
        if open_four_moves:
            return random.choice(open_four_moves)

        return None

    def find_open_fours(self, board, player):
        """Find all open fours for the given player"""
        open_fours = []
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    # Check if placing here would complete an open four
                    for dx, dy in directions:
                        count = 0
                        empty_pos = None
                        valid = True

                        # Check in both directions
                        for step in range(1, 5):
                            x, y = i + step * dx, j + step * dy
                            if 0 <= x < board.l and 0 <= y < board.l:
                                if board.grid[x][y] == player:
                                    count += 1
                                elif board.grid[x][y] == '.':
                                    if empty_pos is None:
                                        empty_pos = (x, y)
                                    else:
                                        valid = False
                                        break
                                else:
                                    valid = False
                                    break
                            else:
                                valid = False
                                break

                        if valid and count == 3 and empty_pos is not None:
                            open_fours.append(empty_pos)

        return open_fours

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

    def alphabeta(self, board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        # Check terminal conditions
        winner = board.hasWinner()
        if winner == self.playerOne:
            return 1000000 + depth  # Prefer faster wins
        elif winner == self.playerTwo:
            return -1000000 - depth  # Prefer slower losses
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
                eval = self.alphabeta(temp_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta<=alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in moves:
                x, y = move
                temp_board = copy.deepcopy(board)
                temp_board.playMove(x, y, self.playerTwo)  # Fixed: was playing playerOne
                eval = self.alphabeta(temp_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta<=alpha:
                    break
            return min_eval

    def evaluate_board(self, board):
        """Improved board evaluation with better pattern detection"""
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        # Evaluate for both players
        score += self.evaluate_player(board, self.playerOne, directions)
        score -= self.evaluate_player(board, self.playerTwo, directions) * 1.1  # Slightly prioritize blocking

        return score

    def evaluate_player(self, board, player, directions):
        """Evaluate board for specific player with better pattern detection"""
        total = 0
        patterns = {}

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == player:
                    for dx, dy in directions:
                        # Check if we've already evaluated this pattern
                        if (0 <= i - dx < board.l and 0 <= j - dy < board.l and
                                board.grid[i - dx][j - dy] == player):
                            continue

                        pattern = self.detect_pattern(board, i, j, dx, dy, player)
                        if pattern:
                            # Special case for open four
                            if pattern == "LIVE_FOUR":
                                # Check if it's really an open four (can win in next move)
                                x, y = i, j
                                count = 0
                                while (0 <= x < board.l and 0 <= y < board.l and
                                       board.grid[x][y] == player):
                                    count += 1
                                    x += dx
                                    y += dy

                                if count >= 4:
                                    total += self.pattern_weights["OPEN_FOUR"]
                            else:
                                total += self.pattern_weights.get(pattern, 0)
        return total

    def detect_pattern(self, board, x, y, dx, dy, player):
        """Improved pattern detection"""
        # Check if this is the start of a pattern
        if (x - dx >= 0 and y - dy >= 0 and
                x - dx < board.l and y - dy < board.l and
                board.grid[x - dx][y - dy] == player):
            return None

        count = 1  # Count the starting piece
        x += dx
        y += dy

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