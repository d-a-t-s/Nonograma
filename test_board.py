import pytest
from createBoard import createBoard

def test_board():
    board = createBoard()
    assert len(board) == 5 
    assert all(len(row) == 5 for row in board)
