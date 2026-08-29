"""Place the R2 and R3 stepping-stone templates on one page.

The upper row contains the two-dimensional regions and the lower row contains
their three-dimensional counterparts for the same alpha values.
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


FIGURES_DIR = Path(__file__).resolve().parents[1]
REGION_2D_DIR = FIGURES_DIR / "region_templates"
REGION_3D_DIR = FIGURES_DIR / "three_dimensional_regions"
for source_directory in (REGION_2D_DIR, REGION_3D_DIR):
    if str(source_directory) not in sys.path:
        sys.path.insert(0, str(source_directory))

from generate_region_templates import (  # noqa: E402
    ALPHAS as ALPHAS_2D,
    GRID_RESOLUTION,
    XLIM,
    YLIM,
    draw_template,
    setup_axis,
)
from generate_three_dimensional_regions import (  # noqa: E402
    ALPHAS as ALPHAS_3D,
    draw_stepping_stone_panel,
)


OUTPUT_STEM = "stepping_stone_region_templates_r2_r3"
COMBINED_FIGSIZE = (16.0, 8.8)
COMBINED_LAYOUT = {
    "left": 0.035,
    "right": 0.995,
    "bottom": 0.015,
    "top": 0.985,
    "wspace": 0.12,
    "hspace": 0.08,
}


def make_combined_templates():
    """Generate the aligned two-row R2/R3 template dashboard."""
    if ALPHAS_2D != ALPHAS_3D:
        raise ValueError("The R2 and R3 template alpha values must match")

    x = np.linspace(XLIM[0], XLIM[1], GRID_RESOLUTION)
    y = np.linspace(YLIM[0], YLIM[1], GRID_RESOLUTION)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=COMBINED_FIGSIZE)
    fig.patch.set_alpha(0)
    grid = fig.add_gridspec(
        2,
        len(ALPHAS_2D),
        height_ratios=(0.9, 1.1),
    )
    fig.subplots_adjust(**COMBINED_LAYOUT)

    for column, alpha in enumerate(ALPHAS_2D):
        axis_2d = fig.add_subplot(grid[0, column])
        setup_axis(axis_2d, alpha)
        draw_template(axis_2d, X, Y, alpha)

        axis_3d = fig.add_subplot(grid[1, column], projection="3d")
        draw_stepping_stone_panel(axis_3d, alpha)

    output_directory = FIGURES_DIR / "generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    pdf_path = output_directory / f"{OUTPUT_STEM}.pdf"
    fig.savefig(
        pdf_path,
        dpi=300,
        transparent=True,
        facecolor="none",
        edgecolor="none",
    )
    plt.close(fig)
    return pdf_path


def main():
    """Build the combined dashboard and print its output path."""
    print(make_combined_templates())


if __name__ == "__main__":
    main()
