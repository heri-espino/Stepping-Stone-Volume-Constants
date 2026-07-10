# Stepping-Stone Volume Constants

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21291269.svg)](https://doi.org/10.5281/zenodo.21291269)

Python tools for evaluating normalized stepping-stone diversion-region volume
constants, validating the numerical results by Monte Carlo simulation, and
reproducing the project figures.

The normalized stepping-stone region is

```math
K_{\mathrm{SS},\alpha}
=
\left\{
z\in\mathbb{R}^d:
\lVert z\rVert^\alpha
+
\lVert z-e_1\rVert^\alpha
\leq 1
\right\}.
```

Its volume is evaluated from the one-dimensional representation

```math
a_{d,\mathrm{SS}}(\alpha)
=
2\kappa_{d-1}
\int_{2^{-1/\alpha}}^1
y_\alpha(u)^{d-1}x_\alpha'(u)\,du,
```

and independently checked using acceptance Monte Carlo sampling in a bounding
cylinder.

For $\alpha=2$, the region is the Gabriel ball with diameter
$[0,e_1]$, and therefore

```math
a_{d,\mathrm{SS}}(2)
=
\frac{\kappa_d}{2^d}.
```

In one dimension, the normalized region has length one.

## Repository contents

```text
stepping_stone_volume/   Theoretical evaluation and Monte Carlo routines
scripts/                 Reproducible experiment entry points
tests/                   Numerical anchor and command-line tests
figures/                 Figure-generation scripts and generated outputs
results/                 Retained validation results
```

## Installation

The project requires Python 3.10 or newer.

### Install in the active environment

From the repository root:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev,figures]"
```

### Install from `requirements.txt`

```powershell
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

### Create an isolated Conda environment

```powershell
conda env create --file environment.yml
conda activate stepping-stone-volume
```

## Monte Carlo validation

Run the default validation experiment:

```powershell
python scripts/run_default_experiment.py
```

To choose the dimensions, parameter values, sample count, and random seed:

```powershell
python -m stepping_stone_volume `
  --dimensions 2 3 4 5 8 `
  --alphas 1.25 1.5 2 3 8 `
  --samples 200000 `
  --seed 20260709 `
  --plot
```

After installation, the command-line interface is also available as:

```powershell
stepping-stone-volume-check
```

A shorter example is:

```powershell
python -m stepping_stone_volume `
  --dimensions 2 3 `
  --alphas 1.5 2
```

CSV files and optional plots are written to `results/`. Each row records:

- the dimension and parameter value;
- the input-specific random seed;
- the sample count and acceptance rate;
- the theoretical and Monte Carlo estimates;
- the Monte Carlo standard error;
- the quadrature error estimate;
- the difference between both evaluations.

The Monte Carlo standard error decreases at the usual rate $N^{-1/2}$.
For higher-precision checks, increase `--samples` to several million per
dimension-parameter pair.

## Reproducing the figures

The figure scripts require NumPy, SciPy, Matplotlib, and a working LaTeX
installation.

To regenerate all figures:

```powershell
python figures/run_all.py
```

Generated figures are written to:

```text
figures/generated/
```

See `figures/README.md` for the correspondence between source scripts and
generated files.

## Tests and package build

Run the test suite with:

```powershell
python -m pytest
```

Build the package with:

```powershell
python -m build
```

GitHub Actions runs the tests and package build on the supported Python
versions.

## Reproducibility notes

- Monte Carlo runs are deterministic for fixed inputs and seeds.
- Each dimension-parameter pair receives a deterministic seed offset.
- Distinct experiments therefore do not reuse the same random stream.
- The theoretical integral uses an endpoint-regularizing substitution for
  stable quadrature when $\alpha>2$.
- Routine generated results are ignored by Git.
- The archived validation CSV files and generated figures used in the
  numerical study are retained in the repository.

## Citation

Citation metadata is provided in `CITATION.cff` and is available through
GitHub's **Cite this repository** interface.

To cite the archived version used by this repository:

> Heriberto Espino-Montelongo and Héctor Maravillo.  
> *Stepping-Stone Volume: Theory, Monte Carlo Validation, and Figures*.  
> Version 1.0.0. Zenodo, 2026.  
> DOI: [10.5281/zenodo.21291269](https://doi.org/10.5281/zenodo.21291269)

BibTeX:

```bibtex
@software{espino_maravillo_2026_stepping_stone,
  author    = {Espino-Montelongo, Heriberto and Maravillo, H{\'e}ctor},
  title     = {Stepping-Stone Volume: Theory, Monte Carlo Validation,
               and Figures},
  year      = {2026},
  version   = {1.0.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21291269},
  url       = {https://doi.org/10.5281/zenodo.21291269}
}
```

## License

This project is released under the MIT License. See `LICENSE`.
