import pytest

from constraints import constraints

m1 = [[True, False, True],
      [False, False, True],
      [True, True, False]]

m2 = [[True, False, True, False, True],
      [False, False, True, True, True],
      [True, True, False, True, False],
      [False, False, False, False, True],
      [True, True, True, True, True]]

def test_constraints_inicialitation():
    assert len(constraints(m1)) != 0
    assert len(constraints(m2)) != 0