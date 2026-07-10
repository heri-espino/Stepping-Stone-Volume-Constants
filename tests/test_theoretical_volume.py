import pytest

from stepping_stone_volume.theoretical_volume import (
    calculate_theoretical_volume,
    unit_ball_volume,
)


def test_d_one_is_unit_interval():
    for alpha in [1.0, 1.25, 2.0, 5.0]:
        assert calculate_theoretical_volume(1, alpha).value == pytest.approx(1.0)


def test_alpha_two_is_gabriel_ball():
    for d in [2, 3, 4, 8, 10]:
        got = calculate_theoretical_volume(d, 2.0).value
        expected = unit_ball_volume(d) / (2.0**d)
        assert got == pytest.approx(expected, rel=1e-13, abs=1e-13)
