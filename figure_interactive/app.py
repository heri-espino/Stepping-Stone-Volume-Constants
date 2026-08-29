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
DEFAULT_REGION_COLOR = "#498FFF"
DEFAULT_OPACITY = 0.58
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


def mix_color(hex_color: str, target: int, amount: float) -> str:
    """Blend a hexadecimal color toward black or white."""
    normalized = hex_color.lstrip("#")
    if len(normalized) != 6:
        normalized = DEFAULT_REGION_COLOR.lstrip("#")
    channels = [int(normalized[offset:offset + 2], 16) for offset in (0, 2, 4)]
    mixed = [round(channel + (target - channel) * amount) for channel in channels]
    return "#" + "".join(f"{channel:02X}" for channel in mixed)


def surface_colorscale(color: str) -> list[list[float | str]]:
    """Create restrained shading around the user-selected surface color."""
    return [
        [0, mix_color(color, 0, 0.2)],
        [0.5, color],
        [1, mix_color(color, 255, 0.34)],
    ]


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


def make_figure(
    alpha: float,
    color: str = DEFAULT_REGION_COLOR,
    opacity: float = DEFAULT_OPACITY,
) -> go.Figure:
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
                colorscale=surface_colorscale(color),
                opacity=opacity,
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
                                    className="number-input alpha-input",
                                ),
                            ],
                            className="slider-row",
                        ),
                    ],
                    className="alpha-control",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Color", htmlFor="region-color"),
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="region-color",
                                            type="color",
                                            value=DEFAULT_REGION_COLOR,
                                        ),
                                        html.Output(
                                            DEFAULT_REGION_COLOR,
                                            id="color-value",
                                        ),
                                    ],
                                    className="color-control",
                                ),
                            ],
                            className="appearance-control",
                        ),
                        html.Div(
                            [
                                html.Label("Opacity", htmlFor="opacity-slider"),
                                html.Div(
                                    [
                                        dcc.Slider(
                                            0,
                                            100,
                                            1,
                                            value=round(DEFAULT_OPACITY * 100),
                                            id="opacity-slider",
                                            marks=None,
                                            tooltip={"always_visible": False},
                                        ),
                                        html.Div(
                                            [
                                                dcc.Input(
                                                    id="opacity-input",
                                                    type="number",
                                                    min=0,
                                                    max=100,
                                                    step=1,
                                                    value=round(DEFAULT_OPACITY * 100),
                                                    className="number-input",
                                                ),
                                                html.Span("%"),
                                            ],
                                            className="percent-input",
                                        ),
                                    ],
                                    className="compact-slider-row",
                                ),
                            ],
                            className="appearance-control opacity-control",
                        ),
                    ],
                    className="appearance-controls",
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
            className="figure-card controls-wrapper",
        ),
    ],
    className="app-shell",
)


@app.callback(
    Output("region-graph", "figure"),
    Output("alpha-input", "value"),
    Output("alpha-slider", "value"),
    Output("opacity-input", "value"),
    Output("opacity-slider", "value"),
    Output("color-value", "children"),
    Input("alpha-slider", "value"),
    Input("alpha-input", "value"),
    Input("region-color", "value"),
    Input("opacity-slider", "value"),
    Input("opacity-input", "value"),
)
def update_region(
    log_alpha: float,
    entered_alpha: float | None,
    color: str,
    opacity_percent: float,
    entered_opacity: float | None,
):
    """Synchronize the alpha and appearance controls with the figure."""
    alpha_input_output = no_update
    alpha_slider_output = no_update
    if ctx.triggered_id == "alpha-input":
        if entered_alpha is None or not np.isfinite(entered_alpha) or entered_alpha <= 0:
            return (no_update,) * 6
        alpha = float(entered_alpha)
        alpha_slider_output = float(np.log10(alpha)) if 1 <= alpha <= 100 else no_update
    elif ctx.triggered_id == "alpha-slider":
        alpha = float(10**log_alpha)
        alpha_input_output = float(f"{alpha:.4g}")
    elif entered_alpha is not None and np.isfinite(entered_alpha) and entered_alpha > 0:
        alpha = float(entered_alpha)
    else:
        alpha = float(10**log_alpha)

    opacity_input_output = no_update
    opacity_slider_output = no_update
    if ctx.triggered_id == "opacity-input":
        if entered_opacity is None or not np.isfinite(entered_opacity) or not 0 <= entered_opacity <= 100:
            return (no_update,) * 6
        opacity = float(entered_opacity) / 100
        opacity_slider_output = entered_opacity
    elif ctx.triggered_id == "opacity-slider":
        opacity = float(opacity_percent) / 100
        opacity_input_output = opacity_percent
    elif entered_opacity is not None and np.isfinite(entered_opacity) and 0 <= entered_opacity <= 100:
        opacity = float(entered_opacity) / 100
    else:
        opacity = DEFAULT_OPACITY

    selected_color = color or DEFAULT_REGION_COLOR
    return (
        make_figure(alpha, selected_color, opacity),
        alpha_input_output,
        alpha_slider_output,
        opacity_input_output,
        opacity_slider_output,
        selected_color.upper(),
    )


if __name__ == "__main__":
    app.run(debug=False)
