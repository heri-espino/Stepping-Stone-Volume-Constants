from __future__ import annotations

# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import betainc
from matplotlib.ticker import MultipleLocator, NullLocator
from pathlib import Path
import sys

from matplotlib.transforms import ScaledTranslation

FIGURES_DIR = Path(__file__).resolve().parents[1]
STYLE_DIR = FIGURES_DIR / "proof_diagram"
if str(STYLE_DIR) not in sys.path:
    sys.path.insert(0, str(STYLE_DIR))

from paper_figure_style import apply_stix_fonts  # noqa: E402

from stepping_stone_volume.theoretical_volume import (
    calculate_theoretical_volume,
    unit_ball_volume,
)

apply_stix_fonts()
plt.rcParams.update({
    "axes.unicode_minus": False,
    "axes.linewidth": 0.75,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

BLADE_RUNNER_NEON_PALETTE = [
    "#206D67",  # Verde teca profundo
    "#56CBB9",  # Cian neón
    "#95B5B3",  # Verde glauco pálido
    "#5380A6",  # Azul cerúleo desaturado
    "#1D4275",  # Azul cobalto industrial
    "#162133",  # Azul medianoche
    "#3C2F47",  # Púrpura profundo
    "#63527D",  # Violeta espectral intermedio
    "#9A7C93",  # Lavanda polvoriento
    "#6F494E",  # Púrpura terracota desaturado
]
# %%


def stepping_stone_volume(dimension: int, alpha: float) -> float:
    """Return only the theoretical volume used by the plotting code."""
    return calculate_theoretical_volume(dimension, float(alpha)).value


def relative_neighborhood_volume(dimension):
    """Volume of the normalized relative-neighborhood lune."""
    return unit_ball_volume(dimension) * betainc(
        (dimension + 1) / 2, 0.5, 0.75
    )


# %%
# -----------------------------
# Alpha values
# -----------------------------
LINEAR_ALPHAS = np.linspace(1.0, 8.0, 421)
LOGX_ALPHAS = np.linspace(1.0, 40.0, 1171)
LINEAR_RELATIVE_NEIGHBORHOOD_X = 9.0
LOG_RELATIVE_NEIGHBORHOOD_X = 60.0


dimensions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 20]
INTERSECTION_ALPHA_TICKS = [
    (7.118390825795, r"$7.12$"),
    (23.643510648, r"$23.64$"),
]
CURVE_LABEL_OFFSETS = {
    "linear": {
        3: (4, 5),
        20: (14, 0),
    },
    "xlog": {
        2: (4, -2),
        4: (4, 2),
        20: (4, 3),
    },
}
RELATIVE_NEIGHBORHOOD_LABEL_Y_OFFSETS = {
    2: -2,
    4: 2,
}


def densify_d2_alpha_grid(alpha_values):
    dense_start = np.linspace(1.0, 2.0, 1201)
    return np.unique(np.concatenate([dense_start, alpha_values[alpha_values > 2.0]]))


# %%
# -----------------------------
# Compute values
# -----------------------------

volume_values_by_dimension = {}

for d in dimensions:
    linear_alphas = densify_d2_alpha_grid(
        LINEAR_ALPHAS) if d == 2 else LINEAR_ALPHAS
    xlog_alphas = densify_d2_alpha_grid(LOGX_ALPHAS) if d == 2 else LOGX_ALPHAS
    volume_values_by_dimension[d] = {
        "linear": {
            "alpha": linear_alphas,
            "volume": np.array(
                [stepping_stone_volume(d, alpha) for alpha in linear_alphas]
            ),
        },
        "xlog": {
            "alpha": xlog_alphas,
            "volume": np.array(
                [stepping_stone_volume(d, alpha) for alpha in xlog_alphas]
            ),
        },
    }


def set_alpha_ticks(ax, xscale, relative_neighborhood_x):
    """Use readable alpha ticks for linear and log-x variants."""
    if xscale == "log":
        x_ticks = [1, 2, 5, 10, 20, 40, relative_neighborhood_x]
        ax.xaxis.set_minor_locator(NullLocator())
    else:
        x_ticks = [1, 2, 3, 4, 5, 6, 7, 8, relative_neighborhood_x]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(i) for i in x_ticks[:-1]] + [r"$\infty$"])


def add_intersection_alpha_ticks(ax):
    xmin, xmax = ax.get_xlim()
    tick_label_transform = (
        ax.get_xaxis_transform()
        + ScaledTranslation(0, -7 / 72, ax.figure.dpi_scale_trans)
    )

    for alpha, label in INTERSECTION_ALPHA_TICKS:
        if not xmin < alpha < xmax:
            continue

        ax.plot(
            [alpha, alpha],
            [0.0, -0.015],
            transform=ax.get_xaxis_transform(),
            color="0.45",
            linewidth=0.7,
            clip_on=False,
            zorder=5,
        )
        ax.text(
            alpha,
            0,
            label,
            transform=tick_label_transform,
            ha="center",
            va="top",
            fontsize=9,
            color="0.45",
            clip_on=False,
        )


def add_x_axis_arrow(ax):
    ax.annotate(
        "",
        xy=(1.002, 0),
        xytext=(0.978, 0),
        xycoords=ax.transAxes,
        textcoords=ax.transAxes,
        arrowprops={
            "arrowstyle": "-|>",
            "color": "black",
            "linewidth": 0.75,
            "mutation_scale": 8,
            "shrinkA": 0,
            "shrinkB": 0,
        },
        clip_on=False,
        zorder=6,
    )


def add_curve_end_label(ax, x, y, d, color, data_key):
    x_offset, y_offset = CURVE_LABEL_OFFSETS.get(data_key, {}).get(d, (4, 0))
    text_transform = (
        ax.transData
        + ScaledTranslation(
            x_offset / 72,
            y_offset / 72,
            ax.figure.dpi_scale_trans,
        )
    )
    ax.text(
        x,
        y,
        fr"$d={d}$",
        transform=text_transform,
        ha="left",
        va="center",
        fontsize=8.5,
        color=color,
        clip_on=False,
    )


def format_relative_neighborhood_volume(value):
    return f"{value:.3g}"


def add_relative_neighborhood_volume_axis(ax, dimension_colors):
    relative_neighborhood_values = [
        relative_neighborhood_volume(d) for d in dimensions
    ]
    volume_axis = ax.twinx()

    volume_axis.set_ylim(ax.get_ylim())
    volume_axis.set_yticks(relative_neighborhood_values)
    volume_axis.set_yticklabels(
        [
            format_relative_neighborhood_volume(value)
            for value in relative_neighborhood_values
        ]
    )
    volume_axis.set_ylabel(
        r"$a_{d,\mathrm{RNG}}$",
        fontsize=9,
        color="0.35",
        labelpad=6,
    )

    volume_axis.spines["top"].set_visible(False)
    volume_axis.spines["left"].set_visible(False)
    volume_axis.spines["right"].set_visible(False)
    volume_axis.tick_params(
        axis="y",
        direction="out",
        length=0,
        width=0,
        color="0.45",
        labelsize=8,
        pad=5,
    )

    for label, d in zip(volume_axis.get_yticklabels(), dimensions):
        label.set_color(dimension_colors[d])
        y_offset = RELATIVE_NEIGHBORHOOD_LABEL_Y_OFFSETS.get(d, 0)
        if y_offset:
            label.set_transform(
                label.get_transform()
                + ScaledTranslation(0, y_offset / 72,
                                    ax.figure.dpi_scale_trans)
            )


def plot_stepping_stone_volume(
    output_stem,
    relative_neighborhood_x,
    data_key,
    xscale="linear",
):
    fontsize = 15
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    dimension_colors = {}

    for color_index, d in enumerate(dimensions):
        alpha_values_d = volume_values_by_dimension[d][data_key]["alpha"]
        y_values = volume_values_by_dimension[d][data_key]["volume"]
        color = BLADE_RUNNER_NEON_PALETTE[
            color_index % len(BLADE_RUNNER_NEON_PALETTE)
        ]
        dimension_colors[d] = color

        line, = ax.plot(
            alpha_values_d,
            y_values,
            color=color,
            linewidth=1.5,
            antialiased=True,
            solid_capstyle="round",
            solid_joinstyle="round",
            label=fr"$d={d}$",
        )
        ax.scatter(
            [relative_neighborhood_x],
            [relative_neighborhood_volume(d)],
            color=line.get_color(),
            s=32,
            antialiased=True,
            zorder=4,
            clip_on=False,
        )
        add_curve_end_label(
            ax,
            alpha_values_d[-1],
            y_values[-1],
            d,
            line.get_color(),
            data_key,
        )

    ax.set_xscale(xscale)
    ax.set_xlabel(r"Parameter $\alpha$", fontsize=fontsize)
    ax.set_ylabel(
        r"Stepping-stone volume $a_{d,\mathrm{SS}}(\alpha)$",
        fontsize=fontsize,
    )
    set_alpha_ticks(ax, xscale, relative_neighborhood_x)

    ax.set_xlim(1, relative_neighborhood_x)
    ax.set_ylim(0, 1.4)
    add_intersection_alpha_ticks(ax)
    add_x_axis_arrow(ax)
    ax.yaxis.set_major_locator(MultipleLocator(0.2))

    ax.grid(
        True,
        which="major",
        linestyle=":",
        linewidth=0.8,
        color="lightgray"
    )

    ax.tick_params(direction="out", length=2.5, width=0.7)
    add_relative_neighborhood_volume_axis(ax, dimension_colors)
    fig.tight_layout()
    output_directory = Path(__file__).resolve().parents[1] / "generated"
    output_directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_directory / f"{output_stem}.pdf", bbox_inches="tight",
                transparent=True, facecolor="none", edgecolor="none")
    plt.close(fig)


# %%
# -----------------------------
# Plot
# -----------------------------
plot_stepping_stone_volume(
    "stepping_stone_volume_linear_scale",
    LINEAR_RELATIVE_NEIGHBORHOOD_X,
    "linear",
)
plot_stepping_stone_volume(
    "stepping_stone_volume_log_scale",
    LOG_RELATIVE_NEIGHBORHOOD_X,
    "xlog",
    xscale="log",
)
