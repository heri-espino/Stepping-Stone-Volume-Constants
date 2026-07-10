# Contributing

Contributions that improve correctness, numerical stability, documentation,
tests, or reproducibility are welcome.

## Development setup

```powershell
conda activate base
python -m pip install -e ".[dev,figures]"
```

Before opening a pull request, run:

```powershell
python -m pytest
python -m build
```

Keep numerical experiments deterministic by recording seeds and all input
parameters. Figure changes should include both the generator update and its
regenerated files under `figures/generated/`.

Please use focused commits and describe any mathematical, numerical, or visual
change in the pull request.
