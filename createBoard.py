import random as rn

def createBoard(num1, num2):
    board = list(map(lambda x: list(map(lambda x: rn.choice([True, False]), range(num1))), range(num2)))

    #Ensure that each column has at least one True
    for j in range(num1):
        if not any(board[i][j] for i in range(num1)):
            board[rn.randrange(0, num1)][j] = True
    
    #Ensure that each row has at least one True
    for i in range(num2):
        if not any(board[i][j] for j in range(num2)):
            board[i][rn.randrange(0, num2)] = True
    
    return board