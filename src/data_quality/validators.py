import re

import pandas as pd


VALID_COUNTRIES = {
    "Bangladesh",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany",
}

VALID_STATUSES = {
    "Active",
    "Inactive",
    "Suspended",
}


def find_missing_values(df):
    return df.isnull().sum()


def find_duplicate_rows(df):
    return df.duplicated().sum()


def find_duplicate_customer_ids(df):
    return df["customer_id"].duplicated().sum()


def find_missing_emails(df):
    return df["email"].isna().sum()


def find_invalid_emails(df):
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    non_missing_emails = df["email"].dropna().astype(str)

    valid_email = non_missing_emails.str.match(
        email_pattern
    )

    return (~valid_email).sum()


def find_invalid_ages(df):
    invalid_age = (df["age"] < 18) | (df["age"] > 100)

    return invalid_age.sum()


def find_invalid_dates(df):
    dates = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )

    return dates.isna().sum()


def find_inconsistent_countries(df):
    return (~df["country"].isin(VALID_COUNTRIES)).sum()


def find_invalid_statuses(df):
    return (~df["customer_status"].isin(VALID_STATUSES)).sum()

def find_missing_phones(df):
    return df["phone"].isna().sum()

def find_missing_income(df):
    return df["annual_income"].isna().sum()

def get_column_quality(df):
    results = []

    for column in df.columns:
        total = len(df)
        missing = df[column].isna().sum()

        completeness = (
            (total - missing) / total * 100
            if total > 0
            else 100
        )

        results.append({
            "column": column,
            "total_rows": total,
            "missing_values": int(missing),
            "completeness": round(completeness, 2),
        })

    return results