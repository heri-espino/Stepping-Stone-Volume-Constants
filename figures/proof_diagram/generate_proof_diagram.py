"""
Generate a midpoint-centered stepping-stone proof figure.

This version is designed to match the proof of the one-dimensional integral
formula.  The normalized region is drawn in shifted coordinates x = X - 1/2,
so the two sites are at (-1/2, 0) and (1/2, 0), and the symmetry line is x = 0.

Main visual ideas:
1. whole stepping-stone region shown with a light fill,
2. right half x >= 0 shown with a darker fill,
3. one representative slice at x = x_alpha(u),
4. half-height y_alpha(u) indicated explicitly,
5. symmetry about x = 0 explains the factor 2.
"""

from pathlib import Path

from paper_figure_style import (
    SAVEFIG_KWARGS,
    TEMPLATE_BOUNDARY_COLOR,
    TEMPLATE_FILL_ALPHA,
    TEMPLATE_FILL_COLOR,
    apply_paper_style,
)
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Visual style.
# ---------------------------------------------------------------------------
REGION_COLOR = TEMPLATE_FILL_COLOR
RIGHT_HALF_COLOR = "#5A7EBA"
BOUNDARY_COLOR = TEMPLATE_BOUNDARY_COLOR
SLICE_COLOR = "#3C2F47"
CONSTRUCTION_COLOR = "#6F494E"
POINT_COLOR = "#000000"
GUIDE_COLOR = "#8F8F8F"
TEXT_COLOR = "#9A7C93"


# ---------------------------------------------------------------------------
# Figure parameters.
# ---------------------------------------------------------------------------
OUTPUT_STEM = "stepping_stone_proof_midpoint"
ALPHA = 3.0
SLICE_U = 0.9
XLIM = (-0.75, 0.75)
YLIM = (-0.75, 0.75)
GRID_RESOLUTION = 3600


apply_paper_style()
plt.rcParams.update({
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.75,
    "axes.unicode_minus": False,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


# ---------------------------------------------------------------------------
# Geometry in midpoint-centered coordinates.
# ---------------------------------------------------------------------------
# In the original normalized configuration the sites are 0 and e_1.
# After shifting by -1/2 e_1, the sites become -1/2 and +1/2 on the x-axis.
# Thus the region becomes
#   {(x,y): ||(x,y)-(-1/2,0)||^alpha + ||(x,y)-(1/2,0)||^alpha <= 1 }.
# ---------------------------------------------------------------------------

def stepping_mask_midpoint(X, Y, alpha):
    """Boolean mask for the midpoint-centered stepping-stone region."""
    d_left = np.sqrt((X + 0.5) ** 2 + Y ** 2)
    d_right = np.sqrt((X - 0.5) ** 2 + Y ** 2)
    return d_left ** alpha + d_right ** alpha <= 1


def x_alpha(u, alpha):
    r"""
    Midpoint-centered longitudinal coordinate of the right-half boundary point.

    x_alpha(u) = (u^2 - (1-u^alpha)^{2/alpha}) / 2.
    """
    return 0.5 * (u ** 2 - (1 - u ** alpha) ** (2 / alpha))


def y_alpha(u, alpha):
    r"""
    Transverse radius at parameter u.

    y_alpha(u) = 1/2 * sqrt(4u^2 - [1 + u^2 - (1-u^alpha)^{2/alpha}]^2).
    """
    inside = 4 * u ** 2 - (
        1 + u ** 2 - (1 - u ** alpha) ** (2 / alpha)
    ) ** 2
    return 0.5 * np.sqrt(max(inside, 0.0))


def rho_alpha(u, alpha):
    r"""
    Distance from the boundary point to the right site.

    rho(u) = (1 - u^alpha)^{1/alpha}.
    """
    return (1 - u ** alpha) ** (1 / alpha)


def annotate_text(ax, text, xy, ha="left", va="top", fontsize=10):
    """Place plain text in data coordinates."""
    ax.text(
        xy[0],
        xy[1],
        text,
        ha=ha,
        va=va,
        fontsize=fontsize,
        linespacing=1.35,
        color=TEXT_COLOR,
    )


def plot_stepping_stone_proof_figure(alpha=ALPHA, u=SLICE_U):
    """Create and save the midpoint-centered proof figure."""
    # Parameter range for the right-half parametrization.
    u0 = 2 ** (-1 / alpha)
    if not (u0 <= u <= 1):
        raise ValueError(
            f"u must satisfy 2^(-1/alpha) <= u <= 1; here u0={u0:.5f}.")

    # Computational grid.
    x = np.linspace(XLIM[0], XLIM[1], GRID_RESOLUTION)
    y = np.linspace(YLIM[0], YLIM[1], GRID_RESOLUTION)
    X, Y = np.meshgrid(x, y)

    # Region masks.
    mask = stepping_mask_midpoint(X, Y, alpha)
    right_mask = mask & (X >= 0)

    # Representative slice geometry.
    x0 = x_alpha(u, alpha)
    y0 = y_alpha(u, alpha)
    rho0 = rho_alpha(u, alpha)

    # Key points.
    left_site = (-0.5, 0.0)
    right_site = (0.5, 0.0)
    midpoint = (0.0, 0.0)
    top_point = (x0, y0)

    fig, ax = plt.subplots(figsize=(5.0, 5.0))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ticks = np.arange(-0.75, 0.751, 0.25)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    # Coordinate guides.
    ax.axhline(0, color=GUIDE_COLOR, linewidth=0.65, zorder=0)
    ax.axvline(0, color=GUIDE_COLOR, linewidth=0.75, zorder=0)

    # Fill the whole region lightly.
    ax.contourf(
        X,
        Y,
        mask.astype(float),
        levels=[0.5, 1.5],
        colors=[REGION_COLOR],
        alpha=TEMPLATE_FILL_ALPHA,
        zorder=1,
    )

    # Overlay the right half more strongly.
    ax.contourf(
        X,
        Y,
        right_mask.astype(float),
        levels=[0.5, 1.5],
        colors=[RIGHT_HALF_COLOR],
        alpha=0.45,
        zorder=2,
    )

    # Boundary.
    ax.contour(
        X,
        Y,
        mask.astype(float),
        levels=[0.5],
        colors=[BOUNDARY_COLOR],
        linewidths=1.65,
        zorder=3,
    )

    # Baseline between sites.
    ax.plot(
        [left_site[0], right_site[0]],
        [0, 0],
        color=POINT_COLOR,
        linewidth=1.0,
        zorder=4,
    )

    # Sites and midpoint.
    ax.scatter(
        [left_site[0], midpoint[0], right_site[0]],
        [left_site[1], midpoint[1], right_site[1]],
        s=[34, 20, 34],
        color=POINT_COLOR,
        zorder=5,
    )

    # Labels for -1/2, 0, 1/2.
    ax.text(-0.56, -0.070, r"$-\frac{1}{2}$", ha="center", va="top")
    ax.text(0.0, -0.070, r"$\mathbf{0}$", ha="center", va="top")
    ax.text(0.56, -0.070, r"$\frac{1}{2}$", ha="center", va="top")

    # Optional site labels.
    ax.text(-0.56, 0.055, r"$p$", ha="center", va="bottom", color=POINT_COLOR)
    ax.text(0.56, 0.055, r"$q$", ha="center", va="bottom", color=POINT_COLOR)

    # Slice at x = x_alpha(u).
    ax.plot([x0, x0], [-y0, y0], color=SLICE_COLOR, linewidth=1.5, zorder=6)
    ax.scatter([x0], [0], s=18, color=SLICE_COLOR, zorder=7)
    ax.text(
        x0 - 0, -0.070, r"$x_\alpha(u)$",
        color=SLICE_COLOR, ha="right", va="top"
    )

    # Half-height y_alpha(u).
    ax.annotate(
        "",
        xy=(x0, y0),
        xytext=(x0, 0),
        arrowprops=dict(arrowstyle="<->", color=SLICE_COLOR, linewidth=1.2),
        zorder=7,
    )
    ax.text(
        x0 - 0.045, 0.5 * y0 - 0.055,
        r"$y_\alpha(u)$",
        color=SLICE_COLOR, ha="right", va="center"
    )

    # Optional full slice length label (helpful in d=2 picture).
    ax.text(
        x0 + 0.09, -y0 - 0.045,
        r"$2y_\alpha(u)$",
        color=SLICE_COLOR, ha="center", va="top"
    )

    # Dashed construction lines to a representative boundary point.
    ax.plot(
        [left_site[0], top_point[0]],
        [left_site[1], top_point[1]],
        color=CONSTRUCTION_COLOR,
        linewidth=1.0,
        linestyle=(0, (4, 3)),
        zorder=5,
    )
    ax.plot(
        [right_site[0], top_point[0]],
        [right_site[1], top_point[1]],
        color=CONSTRUCTION_COLOR,
        linewidth=1.0,
        linestyle=(0, (4, 3)),
        zorder=5,
    )
    ax.scatter([top_point[0]], [top_point[1]], s=24,
               color=CONSTRUCTION_COLOR, zorder=7)

    # Distance labels along the two dashed segments.
    ax.text(
        0.52 * left_site[0] + 0.48 * top_point[0],
        0.52 * left_site[1] + 0.48 * top_point[1] + 0.03,
        r"$u$",
        color=CONSTRUCTION_COLOR,
        ha="center",
        va="bottom",
    )
    ax.text(
        x0 + 0.035,
        0.5 * y0 - 0.055,
        r"$\rho(u)$",
        color=CONSTRUCTION_COLOR,
        ha="left",
        va="center",
    )

    ax.tick_params(direction="out", length=2.5, width=0.7)

    output_directory = Path(__file__).resolve().parents[1] / "generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_directory / f"{OUTPUT_STEM}.pdf",
                bbox_inches="tight", **SAVEFIG_KWARGS)
    plt.close(fig)


if __name__ == "__main__":
    plot_stepping_stone_proof_figure()
