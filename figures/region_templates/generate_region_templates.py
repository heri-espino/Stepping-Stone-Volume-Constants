"""Generate the stepping-stone graph unit-template figure.

The paper uses the normalized template

    K_SS,alpha = {z : ||z||^alpha + ||z-e_1||^alpha <= 1}.

This script illustrates that template for representative values of alpha in
the normalized coordinates p=0 and q=e_1.

Run from this folder with:
    conda run -n base python generate_region_templates.py
"""

from pathlib import Path
import sys

FIGURES_DIR = Path(__file__).resolve().parents[1]
STYLE_DIR = FIGURES_DIR / "proof_diagram"
if str(STYLE_DIR) not in sys.path:
    sys.path.insert(0, str(STYLE_DIR))

from paper_figure_style import (
    SAVEFIG_KWARGS,
    TEMPLATE_BOUNDARY_COLOR,
    TEMPLATE_FILL_ALPHA,
    TEMPLATE_FILL_COLOR,
    THREE_PANEL_FIGSIZE,
    THREE_PANEL_LAYOUT,
    apply_paper_style,
)
import numpy as np
import matplotlib.pyplot as plt


REGION_COLOR = TEMPLATE_FILL_COLOR
BOUNDARY_COLOR = TEMPLATE_BOUNDARY_COLOR
POINT_COLOR = "#111111"
GUIDE_COLOR = "#777777"

OUTPUT_STEM = "stepping_stone_region_templates"
ALPHAS = (1.05, 7.12, 23.64)
XLIM = (-1, 2)
YLIM = (-1, 1)
GRID_RESOLUTION = 3000


apply_paper_style()
plt.rcParams.update({
    "axes.unicode_minus": False,
    "axes.linewidth": 0.75,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


def stepping_stone_mask(X, Y, alpha):
    """Boolean mask for K_SS,alpha in the (0,e_1) normalization."""
    return (X ** 2 + Y ** 2) ** (alpha / 2) + (
        (X - 1) ** 2 + Y ** 2
    ) ** (alpha / 2) <= 1


def setup_axis(ax, alpha):
    """Apply journal-style formatting to one stepping-stone panel."""
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_title(
        rf"$K_{{\mathrm{{SS}},\alpha}}$, $\alpha={alpha:g}$",
        pad=7,
        fontsize=22,
    )
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.axhline(0, color=GUIDE_COLOR, linewidth=0.65, zorder=0)
    ax.axvline(0, color=GUIDE_COLOR, linewidth=0.65, zorder=0)
    ax.plot([0, 1], [0, 0], color=POINT_COLOR, linewidth=0.9, zorder=4)
    ax.scatter([0, 1], [0, 0], s=24, color=POINT_COLOR, zorder=5)
    ax.text(-0.06, -0.03, r"$\mathbf{0}$", ha="center", va="top")
    ax.text(1.08, -0.03, r"$e_1$", ha="center", va="top")
    ax.set_xticks([-1, 0, 1, 2])
    ax.set_yticks([-1, 0, 1])
    ax.tick_params(direction="out", length=2.5, width=0.7, labelsize=10)


def draw_template(ax, X, Y, alpha):
    """Draw one filled stepping-stone template."""
    mask = stepping_stone_mask(X, Y, alpha)
    filled = ax.contourf(
        X,
        Y,
        mask.astype(float),
        levels=[0.5, 1.5],
        colors=[REGION_COLOR],
        alpha=TEMPLATE_FILL_ALPHA,
    )
    filled.set_rasterized(True)
    ax.contour(
        X,
        Y,
        mask.astype(float),
        levels=[0.5],
        colors=[BOUNDARY_COLOR],
        linewidths=1.25,
    )


def generate_region_templates():
    """Create the three-panel stepping-stone unit-template figure."""
    x = np.linspace(XLIM[0], XLIM[1], GRID_RESOLUTION)
    y = np.linspace(YLIM[0], YLIM[1], GRID_RESOLUTION)
    X, Y = np.meshgrid(x, y)

    fig, axes = plt.subplots(1, len(ALPHAS), figsize=THREE_PANEL_FIGSIZE)
    fig.subplots_adjust(**THREE_PANEL_LAYOUT)

    for ax, alpha in zip(axes, ALPHAS):
        setup_axis(ax, alpha)
        draw_template(ax, X, Y, alpha)

    output_directory = Path(__file__).resolve().parents[1] / "generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    pdf_path = output_directory / f"{OUTPUT_STEM}.pdf"
    fig.savefig(pdf_path, dpi=300, **SAVEFIG_KWARGS)
    plt.close(fig)


if __name__ == "__main__":
    generate_region_templates()
