# Publication figures

This directory contains the Python sources for the figures accompanying the
stepping-stone volume calculations. All generators use the project package for
shared numerical calculations where applicable.

## Requirements

Install the project and its figure dependencies from the repository root:

```powershell
conda activate base
python -m pip install -e ".[dev,figures]"
```

Most figures use LaTeX-rendered labels, so a working LaTeX installation with
the `amsmath`, `amssymb`, `fontenc`, `lmodern`, and `stix` packages is required.

## Generate every figure

From any working directory:

```powershell
conda run -n base python path/to/repository/figures/run_all.py
```

The runner stops immediately if a generator fails. All outputs are collected
under `generated/`.

## Source-to-output map

| Source | Output stem |
| --- | --- |
| `region_templates/generate_region_templates.py` | `stepping_stone_region_templates` |
| `three_dimensional_regions/generate_three_dimensional_regions.py` | `stepping_stone_three_dimensional_regions` |
| `volume_curves/generate_volume_curves.py` | `stepping_stone_volume_linear_scale`, `stepping_stone_volume_log_scale` |
| `proof_diagram/generate_proof_diagram.py` | `stepping_stone_proof_midpoint` |

`proof_diagram/paper_figure_style.py` contains shared Matplotlib styling.
