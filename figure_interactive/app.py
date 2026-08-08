"""Interactive three-dimensional stepping-stone region.

Run from the repository root with:

    python figure_interactive/app.py

Then open http://127.0.0.1:8050.  Drag the region to rotate it, or use the
mouse wheel to zoom.
"""

from __future__ import annotations

from pathlib import Path

from dash import Dash, Input, Output, ctx, dcc, html, no_update
import numpy as np
import plotly.graph_objects as go


# These deliberately small grids keep each alpha update quick.
X_COUNT = 72
THETA_COUNT = 64
ALPHA_TICKS = (1, 2, 5, 10, 20, 50, 100)
REGION_COLOR = "#498FFF"
AXIS_COLOR = "#858585"
LABEL_COLOR = "#4F4F4F"
X_AXIS_RANGE = (-0.5, 2.0)
RADIAL_AXIS_RANGE = (-1.25, 1.25)
X_TICK_VALUES = tuple(value for value in np.arange(-0.5, 2.01, 0.25) if value != 0)
RADIAL_TICK_VALUES = tuple(value for value in np.arange(-1.25, 1.26, 0.25) if value != 0)
TICK_SIZE = 0.035


def radius_profile(x_values: np.ndarray, alpha: float) -> np.ndarray:
    """Compute the boundary radius about the x-axis by vectorized bisection."""
    lower = np.zeros_like(x_values)
    upper = np.ones_like(x_values)
    for _ in range(36):
        radius = (lower + upper) / 2
        inside = (
            (x_values**2 + radius**2) ** (alpha / 2)
            + ((1 - x_values) ** 2 + radius**2) ** (alpha / 2)
            <= 1
        )
        lower = np.where(inside, radius, lower)
        upper = np.where(inside, upper, radius)
    return lower


def region_mesh(alpha: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a low-resolution surface of revolution for the requested alpha."""
    x = np.linspace(0, 1, X_COUNT)
    theta = np.linspace(0, 2 * np.pi, THETA_COUNT)
    radius = radius_profile(x, alpha)
    x_grid, theta_grid = np.meshgrid(x, theta)
    return x_grid, radius[None, :] * np.cos(theta_grid), radius[None, :] * np.sin(theta_grid)


def coordinate_frame_traces() -> list[go.Scatter3d]:
    """Create equal, origin-centered axes with quarter-unit ticks."""
    axis_line = go.Scatter3d(
        x=[*X_AXIS_RANGE, None, 0, 0, None, 0, 0],
        y=[0, 0, None, *RADIAL_AXIS_RANGE, None, 0, 0],
        z=[0, 0, None, 0, 0, None, *RADIAL_AXIS_RANGE],
        mode="lines",
        line={"color": AXIS_COLOR, "width": 3},
        hoverinfo="skip",
        showlegend=False,
    )

    tick_x: list[float | None] = []
    tick_y: list[float | None] = []
    tick_z: list[float | None] = []
    for tick in X_TICK_VALUES:
        tick_x.extend([tick, tick, None])
        tick_y.extend([-TICK_SIZE, TICK_SIZE, None])
        tick_z.extend([0, 0, None])
    for tick in RADIAL_TICK_VALUES:
        tick_x.extend([-TICK_SIZE, TICK_SIZE, None, -TICK_SIZE, TICK_SIZE, None])
        tick_y.extend([tick, tick, None, 0, 0, None])
        tick_z.extend([0, 0, None, tick, tick, None])

    tick_marks = go.Scatter3d(
        x=tick_x,
        y=tick_y,
        z=tick_z,
        mode="lines",
        line={"color": AXIS_COLOR, "width": 2},
        hoverinfo="skip",
        showlegend=False,
    )

    positive_radial_ticks = tuple(tick for tick in RADIAL_TICK_VALUES if tick > 0)
    x_labels = [f"{tick:g}" for tick in X_TICK_VALUES]
    radial_labels = [f"{tick:g}" for tick in positive_radial_ticks]
    tick_labels = go.Scatter3d(
        x=[
            *X_TICK_VALUES,
            *(-0.07 * np.ones(len(positive_radial_ticks))),
            *(-0.07 * np.ones(len(positive_radial_ticks))),
        ],
        y=[
            *(0.06 * np.ones(len(X_TICK_VALUES))),
            *positive_radial_ticks,
            *(0.06 * np.ones(len(positive_radial_ticks))),
        ],
        z=[
            *(0.06 * np.ones(len(X_TICK_VALUES))),
            *(0.06 * np.ones(len(positive_radial_ticks))),
            *positive_radial_ticks,
        ],
        mode="text",
        text=[*x_labels, *radial_labels, *radial_labels],
        textfont={"color": "#717784", "size": 9},
        hoverinfo="skip",
        showlegend=False,
    )

    axis_labels = go.Scatter3d(
        x=[1.92, 0, 0], y=[0, 1.18, 0], z=[0, 0, 1.18],
        mode="text",
        text=["x", "y", "z"],
        textfont={"color": LABEL_COLOR, "size": 15},
        hoverinfo="skip",
        showlegend=False,
    )
    return [axis_line, tick_marks, tick_labels, axis_labels]


def make_figure(alpha: float) -> go.Figure:
    """Build the Plotly figure, including the two endpoints of the region."""
    x, y, z = region_mesh(alpha)
    figure = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                surfacecolor=z,
                cmin=-1,
                cmax=1,
                colorscale=[
                    [0, "#2E73DE"],
                    [0.5, REGION_COLOR],
                    [1, "#82B4FF"],
                ],
                opacity=0.58,
                showscale=False,
                hoverinfo="skip",
                lighting={
                    "ambient": 1.0,
                    "diffuse": 0.0,
                    "specular": 0.0,
                    "roughness": 1.0,
                    "fresnel": 0.0,
                },
            ),
            *coordinate_frame_traces(),
            go.Scatter3d(
                x=[0, 1], y=[0, 0], z=[0, 0],
                mode="lines+markers+text",
                line={"color": "#111111", "width": 5},
                marker={"color": "#111111", "size": 5},
                text=["0", "e₁"],
                textposition=["bottom left", "top right"],
                hoverinfo="skip",
                showlegend=False,
            ),
        ]
    )
    figure.update_layout(
        title={
            "text": rf"$K_{{\mathrm{{SS}},\alpha}},\ \alpha = {alpha:.3g}$",
            "x": 0.5,
            "y": 0.97,
            "font": {"family": "Georgia, Times New Roman, serif", "size": 22, "color": "#172033"},
        },
        margin={"l": 0, "r": 0, "t": 52, "b": 8},
        paper_bgcolor="white",
        font={"color": LABEL_COLOR},
        showlegend=False,
        uirevision="stepping-stone-camera",
        scene={
            "bgcolor": "white",
            "xaxis": {"range": list(X_AXIS_RANGE), "visible": False},
            "yaxis": {"range": list(RADIAL_AXIS_RANGE), "visible": False},
            "zaxis": {"range": list(RADIAL_AXIS_RANGE), "visible": False},
            "aspectmode": "cube",
            "camera": {
                "eye": {
                    "x": 0.25,
                    "y": -1.23,
                    "z": 0.62,
                }
            },
        },
    )
    return figure


app = Dash(__name__, assets_folder=Path(__file__).resolve().with_name("assets"))
app.title = "Stepping-stone region"
app.layout = html.Main(
    [
        html.Header(
            [
                html.H1("Three-dimensional stepping-stone region"),
                html.P("Drag to rotate · Scroll to zoom"),
            ],
            className="page-header",
        ),
        html.Section(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("α", htmlFor="alpha-slider"),
                            ],
                            className="control-heading",
                        ),
                        html.Div(
                            [
                                dcc.Slider(
                                    0,
                                    2,
                                    0.01,
                                    value=np.log10(7.12),
                                    id="alpha-slider",
                                    marks={np.log10(tick): str(tick) for tick in ALPHA_TICKS},
                                    tooltip={"always_visible": False},
                                    updatemode="mouseup",
                                    allow_direct_input=False,
                                ),
                                dcc.Input(
                                    id="alpha-input",
                                    type="number",
                                    value=7.12,
                                    debounce=True,
                                    className="alpha-input",
                                ),
                            ],
                            className="slider-row",
                        ),
                    ],
                    className="controls",
                ),
                dcc.Graph(
                    id="region-graph",
                    config={
                        "displaylogo": False,
                        "scrollZoom": True,
                        "modeBarButtonsToRemove": ["select3d", "lasso3d"],
                    },
                    mathjax=True,
                    className="region-graph",
                ),
            ],
            className="figure-card",
        ),
    ],
    className="app-shell",
)


@app.callback(
    Output("region-graph", "figure"),
    Output("alpha-input", "value"),
    Output("alpha-slider", "value"),
    Input("alpha-slider", "value"),
    Input("alpha-input", "value"),
)
def update_region(log_alpha: float, entered_alpha: float | None):
    """Keep the log slider and direct alpha input synchronized."""
    if ctx.triggered_id == "alpha-input":
        if entered_alpha is None or not np.isfinite(entered_alpha) or entered_alpha <= 0:
            return no_update, no_update, no_update
        alpha = float(entered_alpha)
        slider_value = float(np.log10(alpha)) if 1 <= alpha <= 100 else no_update
        return make_figure(alpha), alpha, slider_value

    alpha = float(10**log_alpha)
    displayed_alpha = float(f"{alpha:.4g}")
    return make_figure(alpha), displayed_alpha, no_update


if __name__ == "__main__":
    app.run(debug=False)
