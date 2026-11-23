import hashlib
import sqlite3
from pathlib import Path


def connect_database(
    database_path: Path,
) -> sqlite3.Connection:
    """SQLiteデータベースへ接続する。"""

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(database_path)

    # SQLiteで外部キー制約を有効にする
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database(
    connection: sqlite3.Connection,
) -> None:
    """求人保存用のテーブルを作成する。"""

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collected_at TEXT NOT NULL,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT NOT NULL,
            requirements TEXT NOT NULL,
            role_category TEXT NOT NULL,
            dedup_key TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS job_keywords (
            job_id INTEGER NOT NULL,
            keyword TEXT NOT NULL,

            PRIMARY KEY (job_id, keyword),

            FOREIGN KEY (job_id)
                REFERENCES jobs(id)
                ON DELETE CASCADE
        );
        """
    )

    connection.commit()


def create_dedup_key(
    job: dict[str, str],
) -> str:
    """重複判定に使用するハッシュ値を作成する。"""

    normalized_url = job["url"].strip().rstrip("/").casefold()

    if normalized_url:
        source_text = f"url:{normalized_url}"
    else:
        source_text = "|".join(
            [
                job["title"].casefold(),
                job["company"].casefold(),
                job["location"].casefold(),
                job["requirements"].casefold(),
            ]
        )

    return hashlib.sha256(source_text.encode("utf-8")).hexdigest()


def save_job(
    connection: sqlite3.Connection,
    job: dict[str, str],
    role_category: str,
    keywords: list[str],
) -> bool:
    """
    求人とキーワードを保存する。

    新規保存した場合はTrue、
    重複していた場合はFalseを返す。
    """

    dedup_key = create_dedup_key(job)

    cursor = connection.execute(
        """
        INSERT OR IGNORE INTO jobs (
            collected_at,
            title,
            company,
            location,
            url,
            description,
            requirements,
            role_category,
            dedup_key
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job["collected_at"],
            job["title"],
            job["company"],
            job["location"],
            job["url"],
            job["description"],
            job["requirements"],
            role_category,
            dedup_key,
        ),
    )

    # INSERT OR IGNOREで保存されなかった場合
    if cursor.rowcount == 0:
        return False

    job_id = cursor.lastrowid

    if job_id is None:
        raise RuntimeError("保存した求人のIDを取得できませんでした。")

    connection.executemany(
        """
        INSERT INTO job_keywords (
            job_id,
            keyword
        )
        VALUES (?, ?)
        """,
        [(job_id, keyword) for keyword in keywords],
    )

    return True
