import csv

from stepping_stone_volume import cli


def test_cli_writes_descriptive_csv_columns(tmp_path):
    cli.main(
        [
            "--dimensions",
            "2",
            "--alphas",
            "2",
            "--samples",
            "100",
            "--seed",
            "1",
            "--output-directory",
            str(tmp_path),
        ]
    )

    csv_files = list(tmp_path.glob("stepping_stone_volume_check_*.csv"))
    assert len(csv_files) == 1

    with csv_files[0].open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle))

    assert row["dimension"] == "2"
    assert row["alpha"] == "2.0"
    assert "theoretical_volume" in row
    assert "monte_carlo_estimate" in row


def test_cli_plot_uses_the_only_supported_figure_output(tmp_path, monkeypatch):
    monkeypatch.setattr(
        cli,
        "_plot",
        lambda rows, path: path.touch(),
    )

    cli.main(
        [
            "--dimensions",
            "2",
            "--alphas",
            "2",
            "--samples",
            "100",
            "--seed",
            "1",
            "--output-directory",
            str(tmp_path),
            "--plot",
        ]
    )

    plot_files = [path for path in tmp_path.iterdir() if path.suffix != ".csv"]
    assert len(plot_files) == 1
    assert plot_files[0].suffix == ".pdf"
