"""
Generate a midpoint-centered stepping-stone proof figure.

This version is designed to match the proof of the one-dimensional integral
formula.  The normalized region is drawn in shifted coordinates x = X - 1/2,
so the two sites are at (-1/2, 0) and (1/2, 0), and the symmetry line is x = 0.

Main visual ideas:
1. the two symmetric halves shown with distinct translucent fills,
2. the right half x >= 0 carrying the parametrization,
3. the boundary point z_alpha(u) and its two defining distances,
4. x_alpha(u) shown from the midpoint to the representative slice,
5. the full transverse diameter 2 y_alpha(u).
"""

from pathlib import Path

from paper_figure_style import (
    SAVEFIG_KWARGS,
    apply_paper_style,
)
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Visual style.
# ---------------------------------------------------------------------------
LA_LA_LAND_PALETTE = {
    "HEX": [
        "#030305",
        "#141F1D",
        "#242B4B",
        "#1F4580",
        "#9392C1",
        "#D7A296",
        "#8B5B6D",
        "#B28919",
        "#7C1914",
        "#D6EAFA",
    ]
}

REGION_COLOR = "#7081AE"
RIGHT_HALF_COLOR = "#B3B2D3"
BOUNDARY_COLOR = "#242B4B"
SLICE_COLOR = "#B28919"
Y_VECTOR_COLOR = "#AD8B0D"
X_VECTOR_COLOR = "#7C1914"
CONSTRUCTION_COLOR = "#8B5B6D"
POINT_COLOR = "#030305"
AXES_COLOR = "#000000"
GUIDE_COLOR = "#D3D3D3"
TEXT_COLOR = "#141F1D"
REGION_FILL_ALPHA = 0.42


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
    "text.color": AXES_COLOR,
    "axes.labelcolor": AXES_COLOR,
    "axes.edgecolor": AXES_COLOR,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.75,
    "axes.unicode_minus": False,
    "xtick.color": AXES_COLOR,
    "xtick.labelsize": 10,
    "ytick.color": AXES_COLOR,
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


def label_distance(ax, start, end, text, normal_offset=0.045):
    """Place a distance label parallel to and clear of its segment."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = np.degrees(np.arctan2(dy, dx))
    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180
    angle_radians = np.radians(angle)
    center_x = 0.5 * (start[0] + end[0])
    center_y = 0.5 * (start[1] + end[1])
    ax.text(
        center_x - normal_offset * np.sin(angle_radians),
        center_y + normal_offset * np.cos(angle_radians),
        text,
        color=CONSTRUCTION_COLOR,
        fontsize=8.5,
        ha="center",
        va="center",
        rotation=angle,
        rotation_mode="anchor",
        zorder=7,
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
    left_mask = mask & (X <= 0)
    right_mask = mask & (X >= 0)

    # Representative slice geometry.
    x0 = x_alpha(u, alpha)
    y0 = y_alpha(u, alpha)

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

    # Fill the two symmetric halves with distinct, equally weighted colors.
    ax.contourf(
        X,
        Y,
        left_mask.astype(float),
        levels=[0.5, 1.5],
        colors=[REGION_COLOR],
        alpha=REGION_FILL_ALPHA,
        zorder=1,
    )

    ax.contourf(
        X,
        Y,
        right_mask.astype(float),
        levels=[0.5, 1.5],
        colors=[RIGHT_HALF_COLOR],
        alpha=REGION_FILL_ALPHA,
        zorder=2,
    )

    # Boundary.
    ax.contour(
        X,
        Y,
        mask.astype(float),
        levels=[0.5],
        colors=[BOUNDARY_COLOR],
        linewidths=1.9,
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
        s=[26, 15, 26],
        color=POINT_COLOR,
        zorder=5,
    )

    # Consolidated endpoint and midpoint labels.
    ax.text(-0.54, -0.060, r"$p=\left(-\frac{1}{2},0\right)$", ha="center", va="top", fontsize=9.5)
    ax.text(0.0, -0.070, r"$\mathbf{0}$", ha="center", va="top")
    ax.text(0.54, -0.060, r"$q=\left(\frac{1}{2},0\right)$", ha="center", va="top", fontsize=9.5)

    # The full transverse section has diameter 2 y_alpha(u).
    ax.annotate(
        "",
        xy=(x0, y0),
        xytext=(x0, -y0),
        arrowprops=dict(
            arrowstyle="<->",
            color=Y_VECTOR_COLOR,
            linewidth=1.5,
            shrinkA=0,
            shrinkB=0,
        ),
        zorder=7,
    )
    ax.text(
        x0 + 0.035,
        -0.24,
        r"$2y_\alpha(u)$",
        color=SLICE_COLOR,
        ha="left",
        va="center",
    )

    # The longitudinal coordinate runs from the midpoint to the slice.
    ax.annotate(
        "",
        xy=(x0, 0),
        xytext=midpoint,
        arrowprops=dict(
            arrowstyle="<->",
            color=X_VECTOR_COLOR,
            linewidth=1.3,
            shrinkA=2,
            shrinkB=2,
        ),
        zorder=8,
    )
    ax.scatter([x0], [0], s=14, color=X_VECTOR_COLOR, zorder=9)
    ax.text(
        0.5 * x0,
        -0.035,
        r"$x_\alpha(u)$",
        color=X_VECTOR_COLOR,
        ha="center",
        va="top",
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
    ax.scatter([top_point[0]], [top_point[1]], s=22,
               color=X_VECTOR_COLOR, zorder=8)
    ax.text(
        top_point[0],
        top_point[1] + 0.045,
        r"$z_\alpha(u)$",
        color=X_VECTOR_COLOR,
        ha="center",
        va="bottom",
        zorder=9,
    )

    # Distance labels along the two dashed segments.
    label_distance(
        ax,
        left_site,
        top_point,
        r"$\left\|z_\alpha(u)-p\right\|=u$",
    )
    label_distance(
        ax,
        right_site,
        top_point,
        r"$\left\|z_\alpha(u)-q\right\|=\rho(u)$",
    )

    ax.tick_params(direction="out", length=2.5, width=0.7)

    output_directory = Path(__file__).resolve().parents[1] / "generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_directory / f"{OUTPUT_STEM}.pdf",
                bbox_inches="tight", **SAVEFIG_KWARGS)
    plt.close(fig)


if __name__ == "__main__":
    plot_stepping_stone_proof_figure()
