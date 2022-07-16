from tsptw import solve
from tsptw.types import Requirement, time_t

# cities = [0, 1, 2, 3, 4]
travel_time_matrix: list[list[time_t]] = [
    [0.0, 1.0, 2.0, 5.0, 3.0],
    [1.0, 0.0, 3.0, 20.0, 4.0],
    [2.0, 3.0, 0.0, 4.0, 2.0],
    [5.0, 20.0, 4.0, 0.0, 1.0],
    [3.0, 4.0, 2.0, 1.0, 0.0],
]

requirements = [
    Requirement(0, 100000.0, 0, 0),
    Requirement(0.0, 30.0, 1.0, 1.0),
    Requirement(0.0, 30.0, 1.0, 1.0),
    Requirement(0.0, 7.0, 1.0, 1.0),
    Requirement(0.0, 100000.0, 0.0, 0.0),
]


def test_solve():
    path, score = solve(
        0,
        4,
        [1, 2, 3],
        lambda c: requirements[c],
        lambda c1, c2: travel_time_matrix[c1][c2],
    )

    assert path == [0, 3, 2, 1, 4]
    assert score == 19.0
