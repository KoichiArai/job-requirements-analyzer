import logging
from pathlib import Path

LOGGER_NAME = "job_analyzer"


def configure_logging(
    log_file: Path,
) -> logging.Logger:
    """コンソールとファイルへのログ出力を設定する。"""

    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger(LOGGER_NAME)

    logger.setLevel(logging.INFO)
    logger.propagate = False

    # 同じプロセス内で再設定した場合の重複出力を防ぐ
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(fmt=("%(asctime)s %(levelname)s %(message)s "))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        filename=log_file,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
