"""
Tic Tac Toe Player
"""

import math
import copy 

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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)  
    return X if x_count <= o_count else O

def actions(board):
    
    possibleaction=set()
    for i in range(3):
        for j in range(3):
            if(board[i][j]==EMPTY):
                possibleaction.add((i,j))

    return possibleaction

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j=action
    if board[i][j] is not EMPTY:
        raise ValueError('Invalid Move')

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []

    # Rows, Columns
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])  # columns

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line == [X, X, X]:
            return X
        if line == [O, O, O]:
            return O

    return None

def terminal(board):
    iswinner=winner(board) is not None
    allfilled=all(cell is not EMPTY for row in board for cell in row)
    return iswinner or allfilled

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win==X:
        return 1
    elif win==O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    current_player = player(board)

    def max_value(state):
        if terminal(state):
            return utility(state), None
        v = -math.inf
        best_move = None
        for action in actions(state):
            min_v, _ = min_value(result(state, action))
            if min_v > v:
                v = min_v
                best_move = action
                if v == 1:
                    break  # best possible outcome
        return v, best_move

    def min_value(state):
        if terminal(state):
            return utility(state), None
        v = math.inf
        best_move = None
        for action in actions(state):
            max_v , _ = max_value(result(state, action))
            if max_v < v:
                v = max_v
                best_move = action
                if v == -1:
                    break  # best possible outcome
        return v, best_move

    if current_player == X:
        _ , move = max_value(board)
    else:
        _ , move = min_value(board)

    return move
