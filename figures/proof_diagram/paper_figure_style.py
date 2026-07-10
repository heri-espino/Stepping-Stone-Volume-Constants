"""Shared Matplotlib style for paper figures.

The figures are included in the manuscript after LaTeX scaling, so the
internal point sizes are intentionally larger than the final displayed sizes.
"""

import matplotlib.pyplot as plt
from matplotlib.axes import Axes


_RASTER_PATCHED = False

THREE_PANEL_FIGSIZE = (16, 4.40)
TWO_PANEL_FIGSIZE = (10.08, 3.85)
ONE_PANEL_FIGSIZE = (5.04, 3.85)
TWO_ROW_FIGSIZE = (15.12, 8.0)
THREE_PANEL_LAYOUT = {
    "left": 0.035,
    "right": .99,
    "bottom": 0,
    "top": 1,
    "wspace": 0.14,
}

BASE_FONT_SIZE = 16
TITLE_FONT_SIZE = 22
TICK_FONT_SIZE = 14
SMALL_FONT_SIZE = 13
LEGEND_FONT_SIZE = 13
PANEL_LABEL_FONT_SIZE = 17
SAVEFIG_KWARGS = {"facecolor": "none", "edgecolor": "none"}

TEMPLATE_FILL_COLOR = "#8AA6DA"
TEMPLATE_BOUNDARY_COLOR = "#284FA3"
CONSTRUCTION_BOUNDARY_COLOR = "#456DBA"
TEMPLATE_FILL_ALPHA = 0.7
DENSITY_ALPHA = 0.8
DENSITY_PALETTE = [
    "#1565C0",
    "#FF9800",
    "#009688",
    "#F44336",
    "#448AFF",
    "#8BC34A",
    "#AD1457",
    "#FFC107",
]


def apply_stix_fonts():
    """Use STIX General for text and STIX Math for mathematical notation."""
    plt.rcParams.update({
        "text.usetex": False,
        "font.family": "STIXGeneral",
        "font.serif": ["STIXGeneral"],
        "mathtext.fontset": "stix",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


def apply_paper_style():
    """Use the shared STIX typography and line style for paper figures."""
    apply_stix_fonts()
    _install_rasterized_defaults()
    plt.rcParams.update({
        "font.size": BASE_FONT_SIZE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.75,
        "axes.facecolor": "none",
        "figure.facecolor": "none",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.facecolor": "none",
        "savefig.edgecolor": "none",
        "savefig.transparent": True,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def _set_rasterized(artist):
    if hasattr(artist, "set_rasterized"):
        artist.set_rasterized(True)
    for child in getattr(artist, "collections", []):
        if hasattr(child, "set_rasterized"):
            child.set_rasterized(True)
    return artist


def _install_rasterized_defaults():
    """Rasterize data-heavy artists while keeping axes and labels vector."""
    global _RASTER_PATCHED
    if _RASTER_PATCHED or getattr(Axes, "_pg_rasterized_defaults", False):
        return
    _RASTER_PATCHED = True
    Axes._pg_rasterized_defaults = True

    original_plot = Axes.plot
    original_scatter = Axes.scatter
    original_contourf = Axes.contourf
    original_pcolormesh = Axes.pcolormesh
    original_imshow = Axes.imshow
    original_fill_between = Axes.fill_between

    def plot(self, *args, **kwargs):
        kwargs.setdefault("rasterized", True)
        return original_plot(self, *args, **kwargs)

    def scatter(self, *args, **kwargs):
        kwargs.setdefault("rasterized", True)
        return original_scatter(self, *args, **kwargs)

    def contourf(self, *args, **kwargs):
        return _set_rasterized(original_contourf(self, *args, **kwargs))

    def pcolormesh(self, *args, **kwargs):
        kwargs.setdefault("rasterized", True)
        return original_pcolormesh(self, *args, **kwargs)

    def imshow(self, *args, **kwargs):
        kwargs.setdefault("rasterized", True)
        return original_imshow(self, *args, **kwargs)

    def fill_between(self, *args, **kwargs):
        return _set_rasterized(original_fill_between(self, *args, **kwargs))

    Axes.plot = plot
    Axes.scatter = scatter
    Axes.contourf = contourf
    Axes.pcolormesh = pcolormesh
    Axes.imshow = imshow
    Axes.fill_between = fill_between

    try:
        from mpl_toolkits.mplot3d.axes3d import Axes3D
    except Exception:
        return

    original_plot_surface = Axes3D.plot_surface
    original_plot_trisurf = Axes3D.plot_trisurf

    def plot_surface(self, *args, **kwargs):
        kwargs.setdefault("rasterized", True)
        return original_plot_surface(self, *args, **kwargs)

    def plot_trisurf(self, *args, **kwargs):
        kwargs.setdefault("rasterized", True)
        return original_plot_trisurf(self, *args, **kwargs)

    Axes3D.plot_surface = plot_surface
    Axes3D.plot_trisurf = plot_trisurf


def sans(text):
    """Return text in the shared STIX General figure family."""
    return text
