# Interactive stepping-stone figure

## GitHub Pages version

`index.html` is a static Plotly application. It performs the boundary
calculation in the browser, so it can be served directly by GitHub Pages and
does not require Python or Dash.

[Open the published interactive figure](https://heri-espino.github.io/Stepping-Stone-Volume-Constants/)

To preview it locally, run:

```powershell
python -m http.server --directory figure_interactive
```

Open `http://127.0.0.1:8000`.

## Dash development version

To run the Python/Dash version, install the project dependencies:

```powershell
python -m pip install -e ".[interactive]"
```

Then start the application:

```powershell
python figure_interactive/app.py
```

Open `http://127.0.0.1:8050` in a browser. Move the **α** slider or enter a
positive value in the numeric field to redraw the region. Drag the figure to
rotate it and use the mouse wheel to zoom. The mesh is intentionally low
resolution so updates remain fast.
