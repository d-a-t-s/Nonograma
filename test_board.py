import pytest
from createBoard import createBoard

def test_board():
    n = 6
    board = createBoard(n)
    assert len(board) == n
    assert all(len(row) == n for row in board)

def test_column_has_true():
    n = 5
    board = createBoard(n)
    for j in range(n):
        assert any(board[i][j] for i in range(n))

def test_row_has_true():
    n = 6
    board = createBoard(n)
    for row in board:
        assert any(row)