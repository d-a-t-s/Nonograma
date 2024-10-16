import random as rn

def createBoard():
    board = [[rn.choice([True, False]) for _ in range(5)] for _ in range(5)]

    #Ensure that each column has at least one True
    for j in range(5):
        if not any(board[i][j] for i in range(5)):
            board[rn.randrange(0, 5)][j] = True
    
    #Ensure that each row has at least one True
    for i in range(5):
        if not any(board[i][j] for j in range(5)):
            board[i][rn.randrange(0, 5)] = True
    
    return board