"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Generator comprehension (also list comprehension would work, but would need another calc for building the sum of turns)
    turns = sum(1 for row in board for tile in row if tile != EMPTY)
    # Checking if turns is even or odd
    return X if turns % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Set comprehension
    return {(i, j) for i, row in enumerate(board) for j, tile in enumerate(row) if tile == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Validate action first (no copying yet)
    allowed = actions(board)
    if action not in allowed:
        raise ValueError(f"Invalid action {action}. Allowed: {sorted(allowed)}")

    # Decide the mark based on current player
    mark = player(board)  # X or O

    # Copy only what's needed: a new list of rows (each row copied)
    new_board = [row[:] for row in board]
    new_board[i][j] = mark
    return new_board


def winner(board):
    """
    Returns the winner of the game (X,O), if there is one (None).
    """
    n = len(board)

    # Rows
    for row in board:
        if row[0] != EMPTY and all(tile == row[0] for tile in row):
            return row[0]

    # Columns
    for j in range(n):
        col = [board[i][j] for i in range(n)]
        if col[0] != EMPTY and all(tile == col[0] for tile in col):
            return col[0]

    # Diagonal (top-left to bottom-right)
    if board[0][0] != EMPTY and all(board[i][i] == board[0][0] for i in range(n)):
        return board[0][0]

    # Diagonal (top-right to bottom-left)
    if board[0][n-1] != EMPTY and all(board[i][n-1-i] == board[0][n-1] for i in range(n)):
        return board[0][n-1]

    return None


def terminal(board):
    """
    Returns True if game is over (someone won or tie), False otherwise.
    """
    return winner(board) is not None or not actions(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    champ = winner(board)
    return 1 if champ == X else -1 if champ == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board. If terminal board, return None.
    """

    if terminal(board):
        return None

    current = player(board)  # X maximizes, O minimizes

    def max_value(b, alpha, beta):
        if terminal(b):
            return utility(b)
        v = float("-inf")
        for a in actions(b):
            v = max(v, min_value(result(b, a), alpha, beta))
            alpha = max(alpha, v)
            if v == 1:            # best possible for X; early cutoff
                break
            if alpha >= beta:     # prune
                break
        return v

    def min_value(b, alpha, beta):
        if terminal(b):
            return utility(b)
        v = float("inf")
        for a in actions(b):
            v = min(v, max_value(result(b, a), alpha, beta))
            beta = min(beta, v)
            if v == -1:           # best possible for O; early cutoff
                break
            if alpha >= beta:     # prune
                break
        return v

    best_action = None

    if current == X:
        best_val = float("-inf")
        alpha, beta = float("-inf"), float("inf")
        for a in actions(board):
            val = min_value(result(board, a), alpha, beta)
            if val > best_val:
                best_val, best_action = val, a
            alpha = max(alpha, best_val)
            if best_val == 1:     # can’t do better than a guaranteed win
                break
    else:  # current == O
        best_val = float("inf")
        alpha, beta = float("-inf"), float("inf")
        for a in actions(board):
            val = max_value(result(board, a), alpha, beta)
            if val < best_val:
                best_val, best_action = val, a
            beta = min(beta, best_val)
            if best_val == -1:    # can’t do better than a guaranteed win (for O)
                break

    return best_action
