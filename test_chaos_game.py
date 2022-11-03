import pytest
import numpy as np
from chaos_game import ChaosGame

@pytest.mark.parametrize("n, r", [
    (1, 1/2), (4, -1.5), (4, 1.2)])

def test_different_n_and_r_raises_value_error(n, r):
    with pytest.raises(ValueError):
        ChaosGame(n, r)

@pytest.mark.parametrize("n, r", [
    (0.5, 0.2), (0.2, 0.2), (1, 1), (1, 5)
])
def test_different_n_and_r_raises_type_error(n, r):
    with pytest.raises(TypeError):
        ChaosGame(n, r)

@pytest.mark.parametrize("steps, length, discard", [
    (10, 10, 0), (100, 80, 20), (24, 20, 4)])

def test_iterate(steps, length, discard):
    figure = ChaosGame(n=5)
    x, index = figure.iterate(steps, discard=discard)
    assert(len(x) == length)

