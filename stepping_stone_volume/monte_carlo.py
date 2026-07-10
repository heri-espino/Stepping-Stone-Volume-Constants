from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .theoretical_volume import maximum_transverse_radius, unit_ball_volume


@dataclass(frozen=True)
class MonteCarloResult:
    """Monte Carlo volume estimate."""

    dimension: int
    alpha: float
    samples: int
    hits: int
    bounding_volume: float
    estimate: float
    standard_error: float
    acceptance_rate: float
    seed: int


def estimate_volume_monte_carlo(
    dimension: int,
    alpha: float,
    *,
    samples: int = 200_000,
    seed: int = 20260709,
    chunk_size: int = 1_000_000,
) -> MonteCarloResult:
    """Estimate lambda_d(K_{SS,alpha}) by acceptance Monte Carlo.

    The normalized region is
        K = {z in R^d : ||z||^alpha + ||z-e_1||^alpha <= 1}.

    For d >= 2, we sample uniformly from the cylinder
        [0,1] x B_{d-1}(0,y_max).

    Because the region is rotationally symmetric around the e_1-axis, only
    the transverse radius is sampled; directions are unnecessary.
    """
    if not isinstance(dimension, int) or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    if alpha < 1.0 or not math.isfinite(alpha):
        raise ValueError("alpha must be finite and >= 1")
    if samples < 1:
        raise ValueError("samples must be positive")
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")

    if dimension == 1:
        return MonteCarloResult(
            dimension=dimension,
            alpha=alpha,
            samples=samples,
            hits=samples,
            bounding_volume=1.0,
            estimate=1.0,
            standard_error=0.0,
            acceptance_rate=1.0,
            seed=seed,
        )

    ymax = maximum_transverse_radius(alpha)
    if ymax == 0.0:
        return MonteCarloResult(
            dimension=dimension,
            alpha=alpha,
            samples=samples,
            hits=0,
            bounding_volume=0.0,
            estimate=0.0,
            standard_error=0.0,
            acceptance_rate=0.0,
            seed=seed,
        )

    transverse_dimension = dimension - 1
    bounding_volume = unit_ball_volume(transverse_dimension) * (
        ymax**transverse_dimension
    )  # Cylinder length is 1.
    rng = np.random.default_rng(seed)

    hits = 0
    remaining = samples
    ymax2 = ymax * ymax
    power = alpha / 2.0

    while remaining > 0:
        n = min(chunk_size, remaining)
        x = rng.random(n)

        # If R is the radius in an m-dimensional ball of radius ymax, then
        # P(R <= r) = (r/ymax)^m. Thus R^2 = ymax^2 * U^(2/m).
        u = rng.random(n)
        r2 = ymax2 * np.power(u, 2.0 / transverse_dimension)

        left = np.power(x * x + r2, power)
        right = np.power((1.0 - x) * (1.0 - x) + r2, power)
        inside = (left + right) <= (1.0 + 1e-15)
        hits += int(np.count_nonzero(inside))
        remaining -= n

    p_hat = hits / samples
    estimate = bounding_volume * p_hat
    standard_error = bounding_volume * math.sqrt(max(0.0, p_hat * (1.0 - p_hat)) / samples)

    return MonteCarloResult(
        dimension=dimension,
        alpha=alpha,
        samples=samples,
        hits=hits,
        bounding_volume=bounding_volume,
        estimate=estimate,
        standard_error=standard_error,
        acceptance_rate=p_hat,
        seed=seed,
    )
