import numpy as np
import random


def create_board():
    return np.zeros((3, 3), dtype=int)


def place(board, player, position):
    board[position[0], position[1]] = player


def possibilities(board):
    poss = []
    for index1, row in enumerate(board):
        for index2, item in enumerate(row):
            if item == 0:
                poss.append((index1, index2))
    return poss


def random_place(board, player):
    poss = possibilities(board)
    selection = random.choice(poss)
    place(board, player, selection)


def row_win(board, player):
    for row in board:
        if (row == np.array([player, player, player])).all():
            return True
    return False


def col_win(board, player):
    columns = [[], [], []]
    for index1, row in enumerate(board):
        for index2, item in enumerate(row):
            columns[index2].append(item)
    for col in columns:
        if col == [player, player, player]:
            return True
    return False


def diag_win(board, player):
    diag1 = np.array([board[0, 0], board[1, 1], board[2, 2]])
    diag2 = np.array([board[0, 2], board[1, 1], board[2, 0]])
    winner = np.array([player, player, player])
    if (diag1 == winner).all() or (diag2 == winner).all():
        return True
    return False


def evaluate(board):
    for player in (1, 2):
        if row_win(board, player):
            return player
        if col_win(board, player):
            return player
        if diag_win(board, player):
            return player
    return 0


def play_game():
    board = create_board()
    while possibilities(board):
        for player in (1, 2):
            if not possibilities(board):
                break
            random_place(board, player)
            if evaluate(board) == player:
                print(board)
                return player
    return -1


def play_strategic_game():
    board = create_board()
    board[1, 1] = 1
    while possibilities(board):
        for player in (2, 1):
            if not possibilities(board):
                break
            random_place(board, player)
            if evaluate(board) == player:
                print(board)
                return player
    return -1


results = 0
random.seed(1)
for i in range(1000):
    if play_strategic_game() == 1:
        results += 1
print(results)
