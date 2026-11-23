import pytest

from job_classifier import classify_job


@pytest.mark.parametrize(
    ("title", "expected_role"),
    [
        (
            "Senior QA Automation Engineer",
            "QA Automation",
        ),
        (
            "Software Development Engineer in Test",
            "SDET",
        ),
        (
            "Python Backend Developer",
            "Backend",
        ),
        (
            "Full Stack Developer",
            "Web / Full Stack",
        ),
        (
            "Software QA Engineer",
            "QA / Software Testing",
        ),
        (
            "Product Manager",
            "Others",
        ),
    ],
)
def test_classify_job(
    title: str,
    expected_role: str,
) -> None:
    result = classify_job(title)

    assert result == expected_role
