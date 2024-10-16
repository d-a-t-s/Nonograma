import pytest
from createBoard import createBoard

def test_board():
    board = createBoard()
    assert len(board) == 5 
    assert all(len(row) == 5 for row in board)

def test_columnas_tienen_true_5x5():
    """Verifica que cada columna de un tablero 5x5 tenga al menos un True"""
    tablero = createBoard(5)
    for j in range(5):
        assert any(tablero[i][j] for i in range(5))