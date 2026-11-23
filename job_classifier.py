import re

ROLE_ALIASES: dict[str, tuple[str, ...]] = {
    "SDET": (
        "sdet",
        "software development engineer in test",
    ),
    "QA Automation": (
        "qa automation",
        "quality assurance automation",
        "test automation",
        "automation test engineer",
    ),
    "QA / Software Testing": (
        "qa engineer",
        "quality assurance engineer",
        "software test engineer",
        "test engineer",
        "software tester",
        "qa analyst",
        "test analyst",
    ),
    "Backend": (
        "backend",
        "back-end",
        "back end",
        "server-side",
        "api developer",
    ),
    "Web / Full Stack": (
        "web developer",
        "full stack",
        "full-stack",
        "fullstack",
        "frontend",
        "front-end",
        "front end",
    ),
}


def contains_role_alias(title: str, alias: str) -> bool:
    """求人名に職種名の候補が含まれているか確認する。"""

    escaped_alias = re.escape(alias)

    pattern = (
        rf"(?<![a-zA-Z0-9])"
        rf"{escaped_alias}"
        rf"(?![a-zA-Z0-9])"
    )

    return (
        re.search(
            pattern,
            title,
            flags=re.IGNORECASE,
        )
        is not None
    )


def classify_job(title: str) -> str:

    for role_name, aliases in ROLE_ALIASES.items():
        for alias in aliases:
            if contains_role_alias(title, alias):
                return role_name

    return "Others"
