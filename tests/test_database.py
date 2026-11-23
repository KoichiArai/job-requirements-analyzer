from pathlib import Path

from database import (
    connect_database,
    initialize_database,
    save_job,
)


def test_save_job_does_not_save_duplicate(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "test_job_market.db"

    connection = connect_database(database_path)

    job = {
        "collected_at": "2026-09-01",
        "title": "QA Automation Engineer",
        "company": "Example Systems",
        "location": "Tronrto",
        "url": "https://example.com/jobs/1",
        "description": "Develop automated tests",
        "requirements": "Python Selenium",
    }

    try:
        initialize_database(connection)

        first_result = save_job(
            connection=connection,
            job=job,
            role_category="QA Automation",
            keywords=["Python", "Selenium"],
        )

        second_result = save_job(
            connection=connection,
            job=job,
            role_category="QA Automation",
            keywords=["Python", "Selenium"],
        )

        connection.commit()

        job_count = connection.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]

        keyword_count = connection.execute(
            "SELECT COUNT(*) FROM job_keywords"
        ).fetchone()[0]

    finally:
        connection.close()

    assert first_result is True
    assert second_result is False
    assert job_count == 1
    assert keyword_count == 2
