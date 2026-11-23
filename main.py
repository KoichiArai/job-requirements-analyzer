import argparse
import csv
import re
from datetime import date
from pathlib import Path

from database import (
    connect_database,
    initialize_database,
    save_job,
)
from job_classifier import classify_job
from keyword_extractor import extract_keywords
from logging_config import configure_logging
from report_generator import (
    generate_keyword_report,
    generate_monthly_comparison_report,
)

DEFAULT_INPUT_FILE = Path("data/sample.csv")

DEFAULT_DATABASE_FILE = Path("data/job_market.db")

DEFAULT_REPORTS_DIR = Path("reports")

DEFAULT_LOG_FILE = Path("logs/job_analyzer.log")

DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")

# csvに必要な列
REQUIRED_COLUMNS = {
    "collected_at",
    "title",
    "company",
    "location",
    "url",
    "description",
    "requirements",
}

# 値が空では困る項目
REQUIRED_VALUES = {
    "collected_at",
    "title",
    "company",
    "requirements",
}


def validate_columns(fieldnames: list[str] | None) -> None:
    """csvに必要な列が存在するか確認する"""

    if fieldnames is None:
        raise ValueError("csvにヘッダーがありません。")

    missing_columns = REQUIRED_COLUMNS - set(fieldnames)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))

        raise ValueError(f"csvに必要な列がありません: {missing_text}")


def find_missing_values(row: dict[str, str]) -> list[str]:
    """値が空になっている必須項目を返す。"""

    missing_values = []

    for column_name in REQUIRED_VALUES:
        value = row.get(column_name, "")

        if not value.strip():
            missing_values.append(column_name)

    return sorted(missing_values)


def is_valid_collected_at(value: str) -> bool:
    """取得日がYYYY-MM-DD形式の実在する日付か確認する。"""

    if DATE_PATTERN.fullmatch(value) is None:
        return False

    try:
        date.fromisoformat(value)
    except ValueError:
        return False

    return True


def clean_row(row: dict[str, str]) -> dict[str, str]:
    """各項目の前後にある空白を取り除く。"""

    cleaned = {}

    for column_name, value in row.items():
        if column_name is None:
            continue

        cleaned[column_name] = (value or "").strip()

    return cleaned


def load_jobs(
    file_path: Path,
) -> tuple[list[dict[str, str]], list[str]]:
    """csvを読み込み、正常な求人とエラーを返す。"""

    jobs = []
    errors = []

    with file_path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        validate_columns(reader.fieldnames)

        # 1行目はヘッダなのでデータは2行目から始まる
        for line_number, row in enumerate(reader, start=2):
            cleaned_row = clean_row(row)
            missing_values = find_missing_values(cleaned_row)

            if missing_values:
                missing_text = ", ".join(missing_values)

                errors.append(f"{line_number}行目: 値がありません: {missing_text}")
                continue

            collected_at = cleaned_row["collected_at"]

            if not is_valid_collected_at(collected_at):
                errors.append(
                    f"{line_number}行目: "
                    f"collected_atの日付が不正です: "
                    f"{collected_at} "
                    f"(正しい形式: YYYY-MM-DD)"
                )
                continue

            jobs.append(cleaned_row)

    return jobs, errors


def parse_args(
    arguments: list[str] | None = None,
) -> argparse.Namespace:
    """コマンドライン引数を解析する。"""

    parser = argparse.ArgumentParser(
        description=(
            "求人CSVを読み込み、技術キーワードをSQLiteへ保存してレポートを作成します。"
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help=(f"入力CSVのパス (デフォルト: {DEFAULT_INPUT_FILE})"),
    )

    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE_FILE,
        help=(f"SQLiteデータベースのパス (デフォルト: {DEFAULT_DATABASE_FILE})"),
    )

    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=DEFAULT_REPORTS_DIR,
        help=(f"レポート出力フォルダ (デフォルト: {DEFAULT_REPORTS_DIR})"),
    )

    parser.add_argument(
        "--log-file",
        type=Path,
        default=DEFAULT_LOG_FILE,
        help=(f"ログファイルのパス (デフォルト: {DEFAULT_LOG_FILE})"),
    )

    return parser.parse_args(arguments)


def main() -> None:
    args = parse_args()

    input_file = args.input
    database_file = args.database
    log_file = args.log_file

    report_file = args.reports_dir / "keyword_frequency.csv"

    monthly_report_file = args.reports_dir / "monthly_comparison.csv"

    logger = configure_logging(log_file)

    logger.info(
        "処理開始: input=%s database=%s",
        input_file,
        database_file,
    )

    try:
        jobs, errors = load_jobs(input_file)

    except FileNotFoundError:
        logger.error(
            "入力ファイルが見つかりません: %s",
            input_file,
        )
        return

    except ValueError as error:
        logger.error(
            "入力エラー: %s",
            error,
        )
        return

    logger.info(
        "正常に読み込んだ求人数: %d",
        len(jobs),
    )

    logger.info(
        "除外した求人数: %d",
        len(errors),
    )

    for error in errors:
        logger.warning(
            "求人を除外: %s",
            error,
        )

    connection = connect_database(database_file)

    saved_count = 0
    duplicate_count = 0

    try:
        initialize_database(connection)

        for job in jobs:
            keywords = extract_keywords(job["requirements"])
            role_category = classify_job(job["title"])

            was_interested = save_job(
                connection=connection,
                job=job,
                role_category=role_category,
                keywords=keywords,
            )

            if was_interested:
                saved_count += 1
                save_status = "新規保存"
            else:
                duplicate_count += 1
                save_status = "重複のため保存しない"

            if keywords:
                keyword_text = ", ".join(keywords)
            else:
                keyword_text = "検出なし"

            print("-" * 40)
            logger.info(
                ("求人処理: title=%s role=%s keywords=%s result=%s"),
                job["title"],
                role_category,
                keyword_text,
                save_status,
            )
            print(f"求人名: {job['title']}")
            print(f"職種分類: {role_category}")
            print(f"会社名: {job['company']}")
            print(f"勤務地: {job['location']}")
            print(f"Requirements: {job['requirements']}")

        connection.commit()
        report_row_count = generate_keyword_report(
            connection=connection,
            output_path=report_file,
        )

        comparison_row_count = generate_monthly_comparison_report(
            connection=connection,
            output_path=monthly_report_file,
        )

    finally:
        connection.close()

    print("=" * 40)
    logger.info(
        "処理完了: 新規保存=%d 重複=%d",
        saved_count,
        duplicate_count,
    )
    logger.info(
        "データベース: %s",
        database_file,
    )
    logger.info(
        "キーワードレポート: rows=%d path=%s",
        report_row_count,
        report_file,
    )
    logger.info(
        "前月比較レポート: rows=%d path=%s",
        comparison_row_count,
        monthly_report_file,
    )


if __name__ == "__main__":
    main()
