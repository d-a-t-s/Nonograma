import random as rn

def createBoard(n_cols, n_rows):
    board = list(map(lambda x: list(map(lambda x: rn.choice([True, False]), range(n_cols))), range(n_rows)))

    #Ensure that each column has at least one True
    for j in range(n_cols):
        if not any(board[i][j] for i in range(n_rows)):
            board[rn.randrange(0, n_rows)][j] = True

    #Ensure that each row has at least one True
    for i in range(n_rows):
        if not any(board[i][j] for j in range(n_cols)):
            board[i][rn.randrange(0, n_cols)] = True

    return board