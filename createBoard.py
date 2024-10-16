import random as rn

def createBoard():
    board = [[rn.choice([True, False]) for _ in range(5)] for _ in range(5)]
    
    for j in range(5):
        if not any(board[i][j] for i in range(5)):
            board[rn.randrange(0, 5)][j] = True
    
    return board