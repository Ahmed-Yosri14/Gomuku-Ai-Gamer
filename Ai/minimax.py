import copy
import math
import random
from typing import List, Tuple, Optional


class MiniMax:
    def __init__(self, playerOne: str = 'X', playerTwo: str = 'O', maxDepth: int = 3):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.maxDepth = maxDepth

        self.pattern_weights = {
            "LIVE_TWO": 10,
            "LIVE_THREE": 100,
            "LIVE_FOUR": 10000,
            "DEAD_TWO": 1,
            "DEAD_THREE": 10,
            "DEAD_FOUR": 100,
            "FIVE": 1000000,
            "OPEN_FOUR": 100000
        }

    def FindBestMove(self, board, player) -> Tuple[int, int]:
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
                score = self.minimax(temp_board, self.maxDepth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                score = self.minimax(temp_board, self.maxDepth - 1, True)
                if score < best_score:
                    best_score = score
                    best_move = move

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
        winner = board.hasWinner()
        if winner == self.playerOne:
            return 1000000 + depth
        elif winner == self.playerTwo:
            return -1000000 - depth
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
                temp_board = copy.deepcopy(board)
                temp_board.playMove(x, y, self.playerOne)
                eval = self.minimax(temp_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in moves:
                x, y = move
                temp_board = copy.deepcopy(board)
                temp_board.playMove(x, y, self.playerTwo)
                eval = self.minimax(temp_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, board):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        score += self.evaluate_player(board, self.playerOne, directions)
        score -= self.evaluate_player(board, self.playerTwo, directions) * 1.1

        return score

    def evaluate_player(self, board, player, directions):
        total = 0
        board_size = board.l

        for i in range(board_size):
            for j in range(board_size):
                if board.grid[i][j] == player:
                    for dx, dy in directions:
                        prev_x, prev_y = i - dx, j - dy

                        if (0 <= prev_x < board_size and 0 <= prev_y < board_size and
                                board.grid[prev_x][prev_y] == player):
                            continue

                        pattern = self.detect_pattern(board, i, j, dx, dy, player)
                        if pattern:
                            if pattern == "LIVE_FOUR":
                                x, y = i, j
                                count = 0
                                while (0 <= x < board_size and 0 <= y < board_size and
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