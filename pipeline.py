import sqlite3
from datetime import datetime

import pandas as pd

from src.data_quality.database import DATABASE_PATH
from src.data_quality.metrics import (
    calculate_completeness,
    calculate_consistency,
    calculate_overall_score,
    calculate_uniqueness,
    calculate_validity,
)
from src.data_quality.validators import (
    find_duplicate_customer_ids,
    find_duplicate_rows,
    find_inconsistent_countries,
    find_invalid_ages,
    find_invalid_dates,
    find_invalid_emails,
    find_invalid_statuses,
    find_missing_emails,
    find_missing_income,
    find_missing_phones,
)


DATA_PATH = "data/raw/customers.csv"


def get_severity(issue_count, total_rows):
    issue_rate = issue_count / total_rows

    if issue_rate >= 0.05:
        return "Critical"
    elif issue_rate >= 0.01:
        return "High"
    elif issue_rate >= 0.005:
        return "Medium"
    else:
        return "Low"


def run_pipeline():
    print("\nStarting data quality pipeline...")

    df = pd.read_csv(DATA_PATH)

    total_rows = len(df)
    total_columns = len(df.columns)

    print(f"Loaded {total_rows:,} rows and {total_columns} columns.")

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT dataset_id
        FROM datasets
        WHERE dataset_name = ?
        """,
        ("Customer Dataset",),
    )

    dataset = cursor.fetchone()

    if dataset:
        dataset_id = dataset[0]
    else:
        cursor.execute(
            """
            INSERT INTO datasets (
                dataset_name,
                file_name,
                row_count,
                column_count
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Customer Dataset",
                "customers.csv",
                total_rows,
                total_columns,
            ),
        )

        dataset_id = cursor.lastrowid

    missing_values = (
        df.isnull().sum().sum()
    )

    duplicate_rows = find_duplicate_rows(df)
    duplicate_customer_ids = find_duplicate_customer_ids(df)

    invalid_emails = find_invalid_emails(df)
    invalid_ages = find_invalid_ages(df)
    invalid_dates = find_invalid_dates(df)
    inconsistent_countries = find_inconsistent_countries(df)
    invalid_statuses = find_invalid_statuses(df)

    missing_emails = find_missing_emails(df)
    missing_phones = find_missing_phones(df)
    missing_income = find_missing_income(df)

    completeness = calculate_completeness(df)

    uniqueness = calculate_uniqueness(df)

    validity = calculate_validity(
        invalid_emails=invalid_emails,
        invalid_ages=invalid_ages,
        invalid_dates=invalid_dates,
        invalid_countries=inconsistent_countries,
        invalid_statuses=invalid_statuses,
        total_rows=total_rows,
    )

    consistency = calculate_consistency(
        inconsistent_countries=inconsistent_countries,
        total_rows=total_rows,
    )

    overall_score = calculate_overall_score(
        completeness=completeness,
        validity=validity,
        uniqueness=uniqueness,
        consistency=consistency,
    )

    run_timestamp = datetime.now().isoformat(timespec="seconds")

    cursor.execute(
        """
        INSERT INTO quality_runs (
            dataset_id,
            run_timestamp,
            overall_score
        )
        VALUES (?, ?, ?)
        """,
        (
            dataset_id,
            run_timestamp,
            overall_score,
        ),
    )

    run_id = cursor.lastrowid

    metrics = [
        ("Completeness", completeness),
        ("Validity", validity),
        ("Uniqueness", uniqueness),
        ("Consistency", consistency),
    ]

    cursor.executemany(
        """
        INSERT INTO quality_metrics (
            run_id,
            metric_name,
            metric_value
        )
        VALUES (?, ?, ?)
        """,
        [
            (run_id, name, value)
            for name, value in metrics
        ],
    )

    issues = [
        (
            "email",
            "Missing Email",
            missing_emails,
        ),
        (
            "email",
            "Invalid Email",
            invalid_emails,
        ),
        (
            "phone",
            "Missing Phone",
            missing_phones,
        ),
        (
            "annual_income",
            "Missing Income",
            missing_income,
        ),
        (
            "age",
            "Invalid Age",
            invalid_ages,
        ),
        (
            "signup_date",
            "Invalid Date",
            invalid_dates,
        ),
        (
            "country",
            "Inconsistent Country",
            inconsistent_countries,
        ),
        (
            "customer_status",
            "Invalid Status",
            invalid_statuses,
        ),
        (
            "customer_id",
            "Duplicate Customer ID",
            duplicate_customer_ids,
        ),
        (
            "dataset",
            "Duplicate Row",
            duplicate_rows,
        ),
        (
            "dataset",
            "Missing Values",
            missing_values,
        ),
    ]

    issue_records = []

    for column_name, issue_type, issue_count in issues:
        if issue_count > 0:
            severity = get_severity(
                issue_count,
                total_rows,
            )

            issue_records.append(
                (
                    run_id,
                    column_name,
                    issue_type,
                    int(issue_count),
                    severity,
                )
            )

    cursor.executemany(
        """
        INSERT INTO quality_issues (
            run_id,
            column_name,
            issue_type,
            issue_count,
            severity
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        issue_records,
    )

    connection.commit()
    connection.close()

    print("\n--- PIPELINE COMPLETE ---")
    print(f"Run ID: {run_id}")
    print(f"Overall Score: {overall_score}%")
    print(f"Completeness: {completeness}%")
    print(f"Validity: {validity}%")
    print(f"Uniqueness: {uniqueness}%")
    print(f"Consistency: {consistency}%")
    print(f"Issues Recorded: {len(issue_records)}")


if __name__ == "__main__":
    run_pipeline()