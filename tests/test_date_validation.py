import pytest

from main import is_valid_collected_at


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-10-14", True),
        ("2024-02-29", True),
        ("2026/10/14", False),
        ("2026-2-14", False),
        ("2026-02-30", False),
        ("20261014", False),
        ("", False),
    ],
)
def test_is_valid_collected_at(
    value: str,
    expected: bool,
) -> None:
    result = is_valid_collected_at(value)

    assert result is expected
