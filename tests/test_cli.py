from pathlib import Path

from main import parse_args


def test_parse_args_uses_default_paths() -> None:
    args = parse_args([])

    assert args.input == Path("data/sample.csv")

    assert args.database == Path("data/job_market.db")

    assert args.reports_dir == Path("reports")

    assert args.log_file == Path("logs/job_analyzer.log")


def test_parse_args_accepts_custom_paths() -> None:
    args = parse_args(
        [
            "--input",
            "custom/jobs.csv",
            "--database",
            "custom/jobs.db",
            "--reports-dir",
            "custom/reports",
            "--log-file",
            "custom/job_analyzer.log",
        ]
    )

    assert args.input == Path("custom/jobs.csv")

    assert args.database == Path("custom/jobs.db")

    assert args.reports_dir == Path("custom/reports")

    assert args.log_file == Path("custom/job_analyzer.log")
