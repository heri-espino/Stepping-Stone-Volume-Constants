"""Regenerate every Python-based figure contained in this portable folder."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
FIGURE_GENERATORS = (
    HERE / "region_templates" / "generate_region_templates.py",
    HERE
    / "three_dimensional_regions"
    / "generate_three_dimensional_regions.py",
    HERE
    / "combined_region_templates"
    / "generate_combined_region_templates.py",
    HERE / "volume_curves" / "generate_volume_curves.py",
    HERE / "proof_diagram" / "generate_proof_diagram.py",
)


def main() -> None:
    """Run each generator with this interpreter and its own working folder."""
    for script in FIGURE_GENERATORS:
        print(f"Running {script.relative_to(HERE)}", flush=True)
        subprocess.run(
            [sys.executable, str(script)],
            cwd=script.parent,
            check=True,
        )


if __name__ == "__main__":
    main()
