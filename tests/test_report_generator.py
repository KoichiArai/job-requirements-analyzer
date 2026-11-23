import csv
from pathlib import Path

from database import (
    connect_database,
    initialize_database,
    save_job,
)
from report_generator import (
    generate_monthly_comparison_report,
)


def create_test_job(
    collected_at: str,
    url: str,
) -> dict[str, str]:
    return {
        "collected_at": collected_at,
        "title": "Backend Developer",
        "company": "Example Company",
        "location": "Toronto",
        "url": url,
        "description": "Develop backend services",
        "requirements": "Python",
    }


def test_generate_monthly_comparison_report(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "test.db"
    report_path = tmp_path / "monthly_comparison.csv"

    connection = connect_database(database_path)

    try:
        initialize_database(connection)

        september_job = create_test_job(
            collected_at="2026-09-01",
            url="https://example.com/september",
        )

        october_job = create_test_job(
            collected_at="2026-10-01",
            url="https://example.com/october",
        )

        save_job(
            connection=connection,
            job=september_job,
            role_category="Backend",
            keywords=["Python", "Docker"],
        )

        save_job(
            connection=connection,
            job=october_job,
            role_category="Backend",
            keywords=["Python", "pytest"],
        )
        connection.commit()

        report_row_count = generate_monthly_comparison_report(
            connection=connection,
            output_path=report_path,
        )

    finally:
        connection.close()

    with report_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        rows = list(csv.DictReader(csv_file))

    rows_by_key = {(row["month"], row["keyword"]): row for row in rows}

    assert report_row_count == 5

    october_python = rows_by_key[("2026-10", "Python")]

    assert october_python["previous_month"] == "2026-09"
    assert october_python["job_count"] == "1"
    assert october_python["previous_job_count"] == "1"
    assert october_python["change"] == "0"
    assert october_python["change_percent"] == "0.0"

    october_docker = rows_by_key[("2026-10", "Docker")]

    assert october_docker["job_count"] == "0"
    assert october_docker["previous_job_count"] == "1"
    assert october_docker["change"] == "-1"
    assert october_docker["change_percent"] == "-100.0"

    october_pytest = rows_by_key[("2026-10", "pytest")]

    assert october_pytest["job_count"] == "1"
    assert october_pytest["previous_job_count"] == "0"
    assert october_pytest["change"] == "1"
    assert october_pytest["change_percent"] == ""
