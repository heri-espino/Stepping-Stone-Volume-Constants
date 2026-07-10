from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path

from .monte_carlo import estimate_volume_monte_carlo
from .theoretical_volume import calculate_theoretical_volume


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Compare theoretical stepping-stone volumes with Monte Carlo estimates."
    )
    parser.add_argument(
        "--dimensions",
        "--dims",
        dest="dimensions",
        nargs="+",
        type=int,
        default=[2, 3, 4, 5],
        help="Spatial dimensions to evaluate (default: 2 3 4 5).",
    )
    parser.add_argument(
        "--alphas",
        nargs="+",
        type=float,
        default=[1.25, 1.5, 2.0, 3.0, 8.0],
        help="Stepping-stone alpha values to evaluate.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=200_000,
        help="Monte Carlo samples per dimension-alpha pair.",
    )
    parser.add_argument("--seed", type=int, default=20260709)
    parser.add_argument("--chunk-size", type=int, default=1_000_000)
    parser.add_argument(
        "--output-directory",
        "--outdir",
        dest="output_directory",
        type=Path,
        default=Path("results"),
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Write a diagnostic plot (requires Matplotlib).",
    )
    args = parser.parse_args(argv)

    args.output_directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    csv_path = (
        args.output_directory / f"stepping_stone_volume_check_{stamp}.csv"
    )

    rows = []
    for dimension in args.dimensions:
        for alpha in args.alphas:
            theory = calculate_theoretical_volume(dimension, alpha)
            # Offset the seed by the inputs while preserving reproducibility.
            local_seed = (
                args.seed
                + 1_000_003 * dimension
                + int(round(100_000 * alpha))
            )
            monte_carlo = estimate_volume_monte_carlo(
                dimension,
                alpha,
                samples=args.samples,
                seed=local_seed,
                chunk_size=args.chunk_size,
            )
            difference = monte_carlo.estimate - theory.value
            z_score = (
                difference / monte_carlo.standard_error
                if monte_carlo.standard_error > 0
                else 0.0
            )
            rel_error = (
                difference / theory.value if theory.value != 0 else 0.0
            )
            rows.append(
                {
                    "dimension": dimension,
                    "alpha": alpha,
                    "theoretical_volume": theory.value,
                    "quadrature_absolute_error": theory.abs_error_estimate,
                    "theoretical_method": theory.method,
                    "monte_carlo_estimate": monte_carlo.estimate,
                    "monte_carlo_standard_error": monte_carlo.standard_error,
                    "difference": difference,
                    "relative_error": rel_error,
                    "z_score": z_score,
                    "samples": monte_carlo.samples,
                    "hits": monte_carlo.hits,
                    "acceptance_rate": monte_carlo.acceptance_rate,
                    "bounding_volume": monte_carlo.bounding_volume,
                    "seed": monte_carlo.seed,
                }
            )

    _write_csv(csv_path, rows)
    _print_table(rows)
    print(f"\nCSV written to: {csv_path}")

    if args.plot:
        plot_path = (
            args.output_directory / f"stepping_stone_volume_check_{stamp}.pdf"
        )
        _plot(rows, plot_path)
        print(f"Plot written to: {plot_path}")


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _print_table(rows: list[dict]) -> None:
    headers = [
        "dimension",
        "alpha",
        "theory",
        "MC",
        "SE",
        "diff",
        "rel.err",
        "z",
        "acc.",
    ]
    print("\n" + " ".join(f"{h:>12}" for h in headers))
    print("-" * (13 * len(headers)))
    for r in rows:
        print(
            f"{r['dimension']:12d} "
            f"{r['alpha']:12.4g} "
            f"{r['theoretical_volume']:12.6g} "
            f"{r['monte_carlo_estimate']:12.6g} "
            f"{r['monte_carlo_standard_error']:12.3g} "
            f"{r['difference']:12.3g} "
            f"{r['relative_error']:12.3g} "
            f"{r['z_score']:12.3g} "
            f"{r['acceptance_rate']:12.3g}"
        )


def _plot(rows: list[dict], path: Path) -> None:
    import matplotlib.pyplot as plt

    # One plot: relative error against alpha, with one curve per dimension.
    dimensions = sorted({int(r["dimension"]) for r in rows})
    fig, ax = plt.subplots(figsize=(8, 5))
    for dimension in dimensions:
        sub = sorted(
            (r for r in rows if int(r["dimension"]) == dimension),
            key=lambda r: float(r["alpha"]),
        )
        xs = [float(r["alpha"]) for r in sub]
        ys = [float(r["relative_error"]) for r in sub]
        yerr = [
            abs(
                float(r["monte_carlo_standard_error"])
                / float(r["theoretical_volume"])
            )
            if float(r["theoretical_volume"]) != 0
            else 0.0
            for r in sub
        ]
        ax.errorbar(
            xs,
            ys,
            yerr=yerr,
            marker="o",
            capsize=3,
            label=f"d={dimension}",
        )
    ax.axhline(0.0, linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel("relative error: (MC - theory) / theory")
    ax.set_title("Monte Carlo check of stepping-stone volume formula")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
