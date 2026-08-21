import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/quality.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def create_tables():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL UNIQUE,
            file_name TEXT NOT NULL,
            row_count INTEGER NOT NULL,
            column_count INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            run_timestamp TEXT NOT NULL,
            overall_score REAL NOT NULL,
            FOREIGN KEY (dataset_id)
                REFERENCES datasets(dataset_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            FOREIGN KEY (run_id)
                REFERENCES quality_runs(run_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_issues (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            column_name TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            issue_count INTEGER NOT NULL,
            severity TEXT NOT NULL,
            FOREIGN KEY (run_id)
                REFERENCES quality_runs(run_id)
        )
    """)

    connection.commit()
    connection.close()