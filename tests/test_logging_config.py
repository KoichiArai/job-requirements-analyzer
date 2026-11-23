from pathlib import Path

from logging_config import configure_logging


def test_configure_logging_writes_log_file(
    tmp_path: Path,
) -> None:
    log_file = tmp_path / "test.log"

    logger = configure_logging(log_file)

    try:
        logger.info("logging test")

        for handler in logger.handlers:
            handler.flush()

        content = log_file.read_text(encoding="utf-8")

        assert "INFO" in content
        assert "logging test" in content

    finally:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()
