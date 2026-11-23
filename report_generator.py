import csv
import sqlite3
from pathlib import Path


def generate_keyword_report(
    connection: sqlite3.Connection,
    output_path: Path,
) -> int:
    """月・職種・技術別の求人数をcsvへ出力する。"""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cursor = connection.execute(
        """
        SELECT
            SUBSTR(jobs.collected_at, 1, 7) AS month,
            jobs.role_category,
            job_keywords.keyword,
            COUNT(*) AS job_count
        FROM job_keywords
        INNER JOIN jobs
            ON jobs.id = job_keywords.job_id
        GROUP BY
            SUBSTR(jobs.collected_at, 1, 7),
            jobs.role_category,
            job_keywords.keyword
        ORDER BY
            month,
            jobs.role_category,
            job_count DESC,
            job_keywords.keyword
        """
    )

    rows = cursor.fetchall()

    with output_path.open(
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "month",
                "role_category",
                "keyword",
                "job_count",
            ]
        )

        writer.writerows(rows)

    return len(rows)


def generate_monthly_comparison_report(
    connection: sqlite3.Connection,
    output_path: Path,
) -> int:
    """ｷｰﾜｰﾄﾞ件数を前月と比較してCSVへ出力する。"""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    cursor = connection.execute(
        """
        SELECT
            SUBSTR(jobs.collected_at, 1, 7) AS month,
            job_keywords.keyword,
            COUNT(*) AS job_count
        FROM job_keywords
        INNER JOIN jobs
            ON jobs.id = job_keywords.job_id
        GROUP BY
            SUBSTR(jobs.collected_at, 1, 7),
            job_keywords.keyword
        ORDER BY
            month,
            job_keywords.keyword
        """
    )

    query_rows = cursor.fetchall()

    months = sorted({row[0] for row in query_rows})

    keywords = sorted({row[1] for row in query_rows})

    counts = {(month, keyword): job_count for month, keyword, job_count in query_rows}

    report_rows = []

    for month_index, month in enumerate(months):
        if month_index == 0:
            for keyword in keywords:
                current_count = counts.get(
                    (month, keyword),
                    0,
                )

                if current_count == 0:
                    continue

                report_rows.append(
                    [
                        month,
                        "",
                        keyword,
                        current_count,
                        "",
                        "",
                        "",
                    ]
                )

            # 最初の月の処理が終わったら次の月へ進む
            continue

        previous_month = months[month_index - 1]

        # 2か月目以降の比較処理
        for keyword in keywords:
            current_count = counts.get(
                (month, keyword),
                0,
            )

            previous_count = counts.get(
                (previous_month, keyword),
                0,
            )

            if current_count == 0 and previous_count == 0:
                continue

            change = current_count - previous_count

            if previous_count == 0:
                change_percent = ""
            else:
                change_percent = round(
                    change / previous_count * 100,
                    1,
                )

            report_rows.append(
                [
                    month,
                    previous_month,
                    keyword,
                    current_count,
                    previous_count,
                    change,
                    change_percent,
                ]
            )

    with output_path.open(
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "month",
                "previous_month",
                "keyword",
                "job_count",
                "previous_job_count",
                "change",
                "change_percent",
            ]
        )

        writer.writerows(report_rows)

    return len(report_rows)
