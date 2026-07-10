"""Default experiment runner.

Run from the project root with:

    python scripts/run_default.py
"""

from stepping_stone_volume.cli import main

main([
    "--dimensions", "2", "3", "4", "5", "8",
    "--alphas", "1.25", "1.5", "2", "3", "8",
    "--samples", "200000",
    "--seed", "20260709",
    "--plot",
])
