from parsefile import *

def board_colored_nono():
    palette, board_solved = Colored_grid('2B_50x50.txt')
    col_constraint = []
    row_constraint = []
    
    for i in range(len(board_solved)):
            tempList = []
            aux = None
            counter = 0
            for j in range(len(board_solved[0])):
                if board_solved[i][j] == aux:
                    counter += 1
                elif aux == None:
                    counter += 1
                    aux = board_solved[i][j]
                else:
                    tempList.append((counter, aux))
                    aux = board_solved[i][j]
                    counter = 1
                    continue
            tempList.append((counter, aux))
            row_constraint.append(tempList)
    for j in range(len(board_solved[0])):
            tempList = []
            aux = None
            counter = 0
            for i in range(len(board_solved)):
                if board_solved[i][j] == aux:
                    counter += 1
                elif aux == None:
                    counter += 1
                    aux = board_solved[i][j]
                else:
                    tempList.append((counter, aux))
                    aux = board_solved[i][j]
                    counter = 1
                    continue
            tempList.append((counter, aux))
            col_constraint.append(tempList)
    return palette, col_constraint, row_constraint, board_solved