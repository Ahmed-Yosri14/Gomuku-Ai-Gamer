import copy
import math
import random
from typing import List, Tuple, Optional


class MiniMax:
    def __init__(self, playerOne: str = 'X', playerTwo: str = 'O', maxDepth: int = 3):
        self.transposition_table = {}
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.maxDepth = maxDepth
        self.pattern_weights = {
            "LIVE_TWO": 100,
            "LIVE_THREE": 10000,
            "LIVE_FOUR": 100000,
            "DEAD_TWO": 1,
            "DEAD_THREE": 10,
            "DEAD_FOUR": 1000,
            "FIVE": 100000000,
            "OPEN_FOUR": 10000000
        }
        self.first_move = True  # Added to track if this is the first move

        # for hashing
    def board_to_key(self, board):
        return ''.join(''.join(row) for row in board.grid)

    def FindBestMove(self, board, player) -> Tuple[int, int]:
        if self.first_move and all(board.grid[i][j] == '.' for i in range(board.l) for j in range(board.l)):
            self.first_move = False
            middle = board.l // 2
            return (middle, middle)

        immediate_move = self.check_immediate_moves(board, player)
        if immediate_move:
            self.first_move = False
            return immediate_move

        best_move = None
        best_score = -math.inf if player == self.playerOne else math.inf

        possible_moves = self.get_relevant_moves(board)
        if not possible_moves:
            self.first_move = False
            return self.get_random_move(board)

        for move in possible_moves:
            x, y = move
            if not board.validMove(x, y):
                continue

            board.playMove(x, y, player)
            score = self.minimax(board, self.maxDepth - 1, player != self.playerOne)
            board.undoMove(x, y)
            if player == self.playerOne and score > best_score:
                best_score = score
                best_move = move
            elif player == self.playerTwo and score < best_score:
                best_score = score
                best_move = move

        self.first_move = False
        return best_move if best_move else self.get_random_move(board)

    def check_immediate_moves(self, board, player):
        opponent = self.playerTwo if player == self.playerOne else self.playerOne

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    board.grid[i][j] = player
                    if board.hasWinner() == player:
                        board.grid[i][j] = '.'
                        return (i, j)
                    board.grid[i][j] = '.'

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    board.grid[i][j] = opponent
                    if board.hasWinner() == opponent:
                        board.grid[i][j] = '.'
                        return (i, j)
                    board.grid[i][j] = '.'

        open_four_moves = self.find_open_fours(board, opponent)
        if open_four_moves:
            return random.choice(open_four_moves)

        return None

    def find_open_fours(self, board, player):
        open_fours = []
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    for dx, dy in directions:
                        count = 0
                        empty_pos = None
                        valid = True

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
        valid_moves = []
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    valid_moves.append((i, j))
        return random.choice(valid_moves) if valid_moves else (0, 0)

    def get_relevant_moves(self, board):
        moves = set()

        # First priority: immediate wins or blocks
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == '.':
                    for player in [self.playerOne, self.playerTwo]:
                        board.grid[i][j] = player
                        if board.hasWinner() == player:
                            board.grid[i][j] = '.'
                            return [(i, j)]  # Return immediately for critical moves
                        board.grid[i][j] = '.'

        # Second priority: moves near existing pieces (but more focused)
        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] != '.':
                    # Only check adjacent squares (reduced from 5x5 to 3x3 area)
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < board.l and 0 <= nj < board.l and board.grid[ni][nj] == '.':
                                moves.add((ni, nj))

        return list(moves) if moves else board.possibleMoves()

    def minimax(self, board, depth, is_maximizing):
        key = (self.board_to_key(board), depth, is_maximizing)
        if key in self.transposition_table:
            return self.transposition_table[key]
        winner = board.hasWinner()
        if winner == self.playerOne:
            return 1000000 + depth
        elif winner == self.playerTwo:
            return -1000000 - depth
        elif board.isFull():
            return 0

        if depth == 0:
            return self.evaluate_board(board)

        moves = self.get_relevant_moves(board)

        if is_maximizing:
            max_eval = -math.inf
            for move in moves:
                x, y = move
                board.playMove(x, y, self.playerOne)
                eval = self.minimax(board, depth - 1, False)
                board.undoMove(x,y)
                max_eval = max(max_eval, eval)
            self.transposition_table[key] = max_eval
            return max_eval
        else:
            min_eval = math.inf
            for move in moves:
                x, y = move
                board.playMove(x, y, self.playerTwo)
                eval = self.minimax(board, depth - 1, True)
                board.undoMove(x, y)
                min_eval = min(min_eval, eval)
            self.transposition_table[key] = min_eval
            return min_eval

    def evaluate_board(self, board):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        score += self.evaluate_player(board, self.playerOne, directions)
        score -= self.evaluate_player(board, self.playerTwo, directions) * 1.1

        return score

    def evaluate_player(self, board, player, directions):
        total = 0
        patterns = {}

        for i in range(board.l):
            for j in range(board.l):
                if board.grid[i][j] == player:
                    for dx, dy in directions:
                        if (0 <= i - dx < board.l and 0 <= j - dy < board.l and
                                board.grid[i - dx][j - dy] == player):
                            continue

                        pattern = self.detect_pattern(board, i, j, dx, dy, player)
                        if pattern:
                            if pattern == "LIVE_FOUR":
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
        if (x - dx >= 0 and y - dy >= 0 and
                x - dx < board.l and y - dy < board.l and
                board.grid[x - dx][y - dy] == player):
            return None

        count = 1
        x += dx
        y += dy

        while (0 <= x < board.l and 0 <= y < board.l and
               board.grid[x][y] == player):
            count += 1
            x += dx
            y += dy

        if count < 2:
            return None

        open_start = (x - (count + 1) * dx >= 0 and y - (count + 1) * dy >= 0 and
                      x - (count + 1) * dx < board.l and y - (count + 1) * dy < board.l and
                      board.grid[x - (count + 1) * dx][y - (count + 1) * dy] == '.')

        open_end = (0 <= x < board.l and 0 <= y < board.l and
                    board.grid[x][y] == '.')

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