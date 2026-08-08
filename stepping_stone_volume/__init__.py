"""Theory and Monte Carlo tools for stepping-stone volume constants."""

from .monte_carlo import MonteCarloResult, estimate_volume_monte_carlo
from .theoretical_volume import (
    TheoreticalVolumeResult,
    calculate_theoretical_volume,
    unit_ball_volume,
)

__version__ = "1.1.0"

__all__ = [
    "MonteCarloResult",
    "TheoreticalVolumeResult",
    "calculate_theoretical_volume",
    "estimate_volume_monte_carlo",
    "unit_ball_volume",
]
