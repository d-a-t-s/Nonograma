import pytest

from Constraints import constraints

m1 = [[True, False, True],
    [False, False, True],
    [True, True, False]]

constraints_m1 = [[[1,1], [1], [2]],[[1, 1], [1], [2]]]

m2 = [[True, False, True, False, True],
    [False, False, True, True, True],
    [True, True, False, True, False],
    [False, False, False, False, True],
    [True, True, True, True, True]]

constraints_m2 = [[[1,1,1],[1,1],[2,1],[2,1],[2,2]],[[1,1,1],[3],[2,1],[1],[5]]]

def test_constraints_initialization():
    assert len(constraints(m1)) != 0
    assert len(constraints(m2)) != 0

def test_corresponding_restrictions():
    assert constraints_m1 == constraints(m1)
    assert constraints_m2 == constraints(m2)