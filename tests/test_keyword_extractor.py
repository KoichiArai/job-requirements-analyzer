from keyword_extractor import extract_keywords


def test_extract_keywords_normalizes_aliases() -> None:
    text = "Experience with Python, Postgres, Amazon Web Services and CI-CD."

    result = extract_keywords(text)

    assert result == [
        "Python",
        "PostgreSQL",
        "AWS",
        "CI/CD",
    ]


def test_java_is_not_detected_in_javascript() -> None:
    text = "Experience with JavaScript is required."

    result = extract_keywords(text)

    assert "JavaScript" in result
    assert "Java" not in result


def test_extract_keywords_returns_empty_list() -> None:
    text = "Good communication skills are required."

    result = extract_keywords(text)

    assert result == []
