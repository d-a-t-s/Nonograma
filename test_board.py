import pytest
from createBoard import createBoard

def test_board():
    board = createBoard()
    assert len(board) == 5 
    assert all(len(row) == 5 for row in board)

def test_column_has_true():
    board = createBoard()
    for j in range(5):
        assert any(board[i][j] for i in range(5))