from stepping_stone_volume.monte_carlo import estimate_volume_monte_carlo


def test_monte_carlo_dimension_one_is_exact():
    result = estimate_volume_monte_carlo(1, 3.0, samples=1000, seed=1)
    assert result.estimate == 1.0
    assert result.standard_error == 0.0
