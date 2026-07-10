from __future__ import annotations

from dataclasses import dataclass
import math

from scipy.integrate import quad
from scipy.special import gammaln


@dataclass(frozen=True)
class TheoreticalVolumeResult:
    """Theoretical volume computation result."""

    dimension: int
    alpha: float
    value: float
    abs_error_estimate: float
    method: str


def unit_ball_volume(dimension: int) -> float:
    """Return kappa_d, the volume of the unit ball in R^d.

    Uses
        kappa_d = pi^(d/2) / Gamma(d/2 + 1).
    The convention kappa_0 = 1 is included.
    """
    if not isinstance(dimension, int) or dimension < 0:
        raise ValueError("dimension must be a nonnegative integer")
    if dimension == 0:
        return 1.0
    return math.exp(
        (dimension / 2.0) * math.log(math.pi)
        - gammaln(dimension / 2.0 + 1.0)
    )


def u0(alpha: float) -> float:
    _validate_alpha(alpha)
    return 2.0 ** (-1.0 / alpha)


def x_alpha(u: float, alpha: float) -> float:
    """Midpoint-centered longitudinal boundary coordinate."""
    _validate_alpha(alpha)
    t = max(0.0, 1.0 - u**alpha)
    return 0.5 * (u * u - t ** (2.0 / alpha))


def y_alpha(u: float, alpha: float) -> float:
    """Transverse boundary radius in the right half of the region."""
    _validate_alpha(alpha)
    t = max(0.0, 1.0 - u**alpha)
    rho2 = t ** (2.0 / alpha)
    inside = 4.0 * u * u - (1.0 + u * u - rho2) ** 2
    # Numerical roundoff can make inside slightly negative at endpoints.
    return 0.5 * math.sqrt(max(0.0, inside))


def x_alpha_prime(u: float, alpha: float) -> float:
    """Derivative of x_alpha.

    For alpha > 2 the derivative has an integrable endpoint singularity at u=1.
    A point value at the endpoint is irrelevant for quadrature.
    """
    _validate_alpha(alpha)
    if u >= 1.0:
        return 0.0
    t = max(0.0, 1.0 - u**alpha)
    return u + (u ** (alpha - 1.0)) * (t ** ((2.0 - alpha) / alpha))


def calculate_theoretical_volume(
    dimension: int,
    alpha: float,
    *,
    epsabs: float = 1e-11,
    epsrel: float = 1e-11,
    limit: int = 300,
) -> TheoreticalVolumeResult:
    """Compute a_{d,SS}(alpha) from the one-dimensional integral.

    The paper formula is

        a = 2 kappa_{d-1} int_{u0}^1 y_alpha(u)^(d-1) x_alpha'(u) du.

    Numerically, this implementation evaluates the same integral after the
    endpoint-regularizing substitution

        t = (1 - u^alpha)^(1/alpha),     u = (1 - t^alpha)^(1/alpha).

    This removes the integrable singularity of x_alpha'(u) at u=1 when
    alpha > 2.  The mathematical value is unchanged.
    """
    _validate_dimension(dimension)
    _validate_alpha(alpha)

    if dimension == 1:
        return TheoreticalVolumeResult(
            dimension=dimension,
            alpha=alpha,
            value=1.0,
            abs_error_estimate=0.0,
            method="exact dimension=1",
        )

    if alpha == 1.0:
        return TheoreticalVolumeResult(
            dimension=dimension,
            alpha=alpha,
            value=0.0,
            abs_error_estimate=0.0,
            method="exact alpha=1 degeneracy",
        )

    # Anchor case: Gabriel ball with diameter [0,e_1].
    if abs(alpha - 2.0) <= 1e-14:
        return TheoreticalVolumeResult(
            dimension=dimension,
            alpha=alpha,
            value=unit_ball_volume(dimension) / (2.0**dimension),
            abs_error_estimate=0.0,
            method="exact alpha=2",
        )

    upper = u0(alpha)

    def integrand_in_t(t: float) -> float:
        # t is rho = ||z-e_1|| on the right-half boundary.
        # u is ||z||, with u^alpha + t^alpha = 1.
        if t <= 0.0:
            return 0.0
        u = max(0.0, 1.0 - t**alpha) ** (1.0 / alpha)

        # Midpoint-centered coordinate and transverse radius.
        x = 0.5 * (u * u - t * t)
        X = x + 0.5
        y2 = u * u - X * X
        y = math.sqrt(max(0.0, y2))

        # Since x(t) decreases from 1/2 to 0 as t increases,
        # |dx/dt| = t + u^(2-alpha) t^(alpha-1).
        jac = t + (u ** (2.0 - alpha)) * (t ** (alpha - 1.0))
        return (y ** (dimension - 1)) * jac

    integral, err = quad(
        integrand_in_t,
        0.0,
        upper,
        epsabs=epsabs,
        epsrel=epsrel,
        limit=limit,
        points=[0.0, upper],
    )
    value = 2.0 * unit_ball_volume(dimension - 1) * integral
    return TheoreticalVolumeResult(
        dimension=dimension,
        alpha=alpha,
        value=value,
        abs_error_estimate=2.0 * unit_ball_volume(dimension - 1) * err,
        method="quad formula with endpoint-regularizing t-substitution",
    )


def maximum_transverse_radius(alpha: float) -> float:
    """Maximum transverse radius of K_{SS,alpha} for alpha >= 1."""
    _validate_alpha(alpha)
    inside = 2.0 ** (-2.0 / alpha) - 0.25
    return math.sqrt(max(0.0, inside))


def _validate_dimension(dimension: int) -> None:
    if not isinstance(dimension, int) or dimension < 1:
        raise ValueError("dimension must be a positive integer")


def _validate_alpha(alpha: float) -> None:
    if not math.isfinite(alpha) or alpha < 1.0:
        raise ValueError("alpha must be finite and >= 1")
