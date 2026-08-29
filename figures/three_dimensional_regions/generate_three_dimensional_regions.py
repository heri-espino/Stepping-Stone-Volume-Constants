"""Generate a three-dimensional stepping-stone region dashboard.

This script reproduces the three-dimensional template panel style for the
stepping-stone region

    K_SS,alpha = {z : ||z||^alpha + ||z-e_1||^alpha <= 1}

and places alpha = 1.25, 2, and 10 side by side.

Run from this folder with:
    conda run -n base python generate_three_dimensional_regions.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")


FIGURES_DIR = Path(__file__).resolve().parents[1]
STYLE_DIR = FIGURES_DIR / "proof_diagram"
if str(STYLE_DIR) not in sys.path:
    sys.path.insert(0, str(STYLE_DIR))

from paper_figure_style import (  # noqa: E402
    ALPHA_REGION_COLORS,
    SMALL_FONT_SIZE,
    TITLE_FONT_SIZE,
    apply_paper_style,
    restore_color_intensity_hsv,
)


OUTPUT_STEM = "stepping_stone_three_dimensional_regions"
ALPHAS = (1.25, 2.0, 10.0)

POINT_COLOR = "#111111"
AXIS_COLOR = "#858585"
TICK_COLOR = "#747474"
LABEL_COLOR = "#4F4F4F"
SURFACE_ALPHA = 0.5
AXIS_ALPHA = 1
TICK_ALPHA = 1

DEFAULT_THETA_COUNT = 128
DEFAULT_X_COUNT = 170
MESH_COUNTS = {
    1.25: (240, 180),
    2.0: (300, 220),
    10.0: (440, 320),
}
THREE_D_FIGSIZE = (16.0, 5.10)
THREE_D_LAYOUT = {
    "left": 0.02,
    "right": 0.995,
    "bottom": 0.0,
    "top": 1.0,
    "wspace": 0.07,
}
THREE_D_PANEL_ZOOM = 1.3
VIEW_X = (-0.65, 1.65)
VIEW_Y = (-1.15, 1.15)
VIEW_Z = (-1, 1)
TITLE_Y = 0.95
VIEW_ELEVATION = 30
VIEW_AZIMUTH = -80

X_AXIS_RANGE = (-0.5, 1.5)
Y_AXIS_RANGE = (-1.0, 1.0)
Z_AXIS_RANGE = (-1.0, 1.0)
X_TICKS = (-0.5, 0.5, 1.0, 1.5)
Y_TICKS = (-1.0, -0.5, 0.5, 1.0)
Z_TICKS = (-1.0, -0.5, 0.5, 1.0)


apply_paper_style()


def ss_radius_profile(x_values, alpha):
    """Solve the three-dimensional boundary radius for x in [0, 1]."""
    radii = np.zeros_like(x_values, dtype=float)
    for idx, x in enumerate(x_values):
        lo = 0.0
        hi = 1.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            value = (x * x + mid * mid) ** (alpha / 2.0) + (
                (1.0 - x) ** 2 + mid * mid
            ) ** (alpha / 2.0)
            if value <= 1.0:
                lo = mid
            else:
                hi = mid
        radii[idx] = lo
    return radii


def surface_of_revolution(x_values, radius_values, theta_values):
    """Return X, Y, Z arrays for a surface of revolution about the x-axis."""
    X, theta = np.meshgrid(x_values, theta_values)
    radius = np.tile(radius_values, (len(theta_values), 1))
    Y = radius * np.cos(theta)
    Z = radius * np.sin(theta)
    return X, Y, Z


def plot_surface(ax, X, Y, Z, color):
    """Plot a translucent Stepping Stone surface."""
    compensated_color = restore_color_intensity_hsv(color, SURFACE_ALPHA)
    ax.plot_surface(
        X,
        Y,
        Z,
        color=compensated_color[:3],
        alpha=compensated_color[3],
        linewidth=0.0,
        antialiased=True,
        shade=True,
        rstride=1,
        cstride=1,
        rasterized=True,
        zorder=3,
    )


def draw_axes(ax):
    """Draw the quiet 3D coordinate frame used by the existing dashboard."""
    tick_length = 0.055

    ax.plot(
        list(X_AXIS_RANGE),
        [0, 0],
        [0, 0],
        color=AXIS_COLOR,
        linewidth=0.8,
        alpha=AXIS_ALPHA,
        zorder=0,
    )
    ax.plot(
        [0, 0],
        list(Y_AXIS_RANGE),
        [0, 0],
        color=AXIS_COLOR,
        linewidth=0.75,
        alpha=AXIS_ALPHA,
        zorder=0,
    )
    ax.plot(
        [0, 0],
        [0, 0],
        list(Z_AXIS_RANGE),
        color=AXIS_COLOR,
        linewidth=0.75,
        alpha=AXIS_ALPHA,
        zorder=0,
    )

    for tick in X_TICKS:
        ax.plot(
            [tick, tick],
            [0, 0],
            [-tick_length, tick_length],
            color=TICK_COLOR,
            linewidth=0.55,
            alpha=TICK_ALPHA,
            zorder=1,
        )
    for tick in Y_TICKS:
        ax.plot(
            [-tick_length, tick_length],
            [tick, tick],
            [0, 0],
            color=TICK_COLOR,
            linewidth=0.55,
            alpha=TICK_ALPHA,
            zorder=1,
        )
    for tick in Z_TICKS:
        ax.plot(
            [-tick_length, tick_length],
            [0, 0],
            [tick, tick],
            color=TICK_COLOR,
            linewidth=0.55,
            alpha=TICK_ALPHA,
            zorder=1,
        )

    ax.text(X_AXIS_RANGE[1] - 0.08, 0.00, 0.18, r"$x$",
            fontsize=SMALL_FONT_SIZE, color=LABEL_COLOR)
    ax.text(-0.05, Y_AXIS_RANGE[1], 0.18, r"$y$",
            fontsize=SMALL_FONT_SIZE, color=LABEL_COLOR)
    ax.text(-0.18, 0.00, Z_AXIS_RANGE[1] - 0.20, r"$z$",
            fontsize=SMALL_FONT_SIZE, color=LABEL_COLOR)


def alpha_label(alpha):
    """Return a compact alpha label for titles and filenames."""
    return f"{alpha:g}"


def draw_stepping_stone_panel(ax, alpha):
    """Draw one three-dimensional stepping-stone template panel."""
    draw_axes(ax)

    ax.plot([0, 1], [0, 0], [0, 0], color=POINT_COLOR,
            linewidth=1.25, zorder=2)

    x_count, theta_count = MESH_COUNTS.get(
        alpha,
        (DEFAULT_X_COUNT, DEFAULT_THETA_COUNT),
    )
    theta = np.linspace(0.0, 2.0 * np.pi, theta_count)
    x = np.linspace(0.0, 1.0, x_count)
    radius = ss_radius_profile(x, alpha)
    plot_surface(
        ax,
        *surface_of_revolution(x, radius, theta),
        color=ALPHA_REGION_COLORS[alpha],
    )

    ax.scatter([0, 1], [0, 0], [0, 0], s=30,
               color=POINT_COLOR, depthshade=False, zorder=4)
    ax.text(-0.05, -0.08, 0.13, r"$\mathbf{0}$", ha="right", va="top", fontsize=SMALL_FONT_SIZE)
    ax.text(1.04, 0.18, 0, r"$e_1$", ha="left", va="top", color='#000000')

    ax.text2D(
        0.5,
        TITLE_Y,
        rf"$K_{{\mathrm{{SS}},\alpha}}$, $\alpha={alpha_label(alpha)}$",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=TITLE_FONT_SIZE+2,
    )

    ax.set_box_aspect(
        (
            VIEW_X[1] - VIEW_X[0],
            VIEW_Y[1] - VIEW_Y[0],
            VIEW_Z[1] - VIEW_Z[0],
        ),
        zoom=THREE_D_PANEL_ZOOM,
    )
    ax.set_anchor("C")
    ax.view_init(elev=VIEW_ELEVATION, azim=VIEW_AZIMUTH)
    ax.set_xlim(*VIEW_X)
    ax.set_ylim(*VIEW_Y)
    ax.set_zlim(*VIEW_Z)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 0.0))
        axis.pane.set_edgecolor((1.0, 1.0, 1.0, 0.0))
        axis.line.set_color((1.0, 1.0, 1.0, 0.0))
        axis.line.set_linewidth(0.0)


def make_dashboard():
    """Create and save the three-alpha, three-dimensional dashboard."""
    fig = plt.figure(figsize=THREE_D_FIGSIZE)
    fig.patch.set_alpha(0)
    grid = fig.add_gridspec(1, len(ALPHAS), width_ratios=(1.0, 1.0, 1.0))
    fig.subplots_adjust(**THREE_D_LAYOUT)

    for col, alpha in enumerate(ALPHAS):
        ax = fig.add_subplot(grid[0, col], projection="3d")
        draw_stepping_stone_panel(ax, alpha)

    output_directory = Path(__file__).resolve().parents[1] / "generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    pdf_path = output_directory / f"{OUTPUT_STEM}.pdf"

    fig.savefig(pdf_path, dpi=300, transparent=True,
                facecolor="none", edgecolor="none")
    plt.close(fig)

    return pdf_path


def main():
    """Build the dashboard and print the saved output."""
    print(make_dashboard())


if __name__ == "__main__":
    main()
