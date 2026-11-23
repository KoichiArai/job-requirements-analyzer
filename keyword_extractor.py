import re

# 分析結果に表示する名前と、求人票内で想定される表記
KEYWORD_ALIASES: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "Java": ("java",),
    "JavaScript": (
        "javascript",
        "java script",
    ),
    "FastAPI": (
        "fastapi",
        "fast api",
    ),
    "PostgreSQL": (
        "postgresql",
        "postgres",
    ),
    "Docker": ("docker",),
    "Redis": ("redis",),
    "AWS": (
        "aws",
        "amazon web services",
    ),
    "Git": (
        "git",
        "github",
        "gitlab",
    ),
    "GitHub Actions": (
        "github actions",
        "github action",
    ),
    "CI/CD": (
        "ci/cd",
        "ci-cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment",
    ),
    "pytest": (
        "pytest",
        "py.test",
    ),
    "Selenium": ("selenium",),
    "Playwright": ("playwright",),
    "Jenkins": ("jenkins",),
    "REST API": (
        "rest api",
        "restful api",
        "restful services",
    ),
    "API Testing": (
        "api testing",
        "api test",
        "api automation",
    ),
}


def contains_alias(text: str, alias: str) -> bool:
    """文章内に指定した技術名が含まれているか確認する"""

    escaped_alias = re.escape(alias)

    pattern = (
        rf"(?<![a-zA-Z0-9])"
        rf"{escaped_alias}"
        rf"(?![a-zA-Z0-9])"
    )

    return (
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
        is not None
    )


def extract_keywords(text: str) -> list[str]:
    """文章から技術キーワードを抽出する。"""

    detected_keywords = []

    for canonical_name, aliases in KEYWORD_ALIASES.items():
        for alias in aliases:
            if contains_alias(text, alias):
                detected_keywords.append(canonical_name)
                break

    return detected_keywords
