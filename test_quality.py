import pandas as pd

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
    find_missing_values,
    get_column_quality,
)


df = pd.read_csv("data/raw/customers.csv")


print("\n--- DATA QUALITY CHECK ---")

print(
    "Missing values:",
    find_missing_values(df).sum()
)

print(
    "Duplicate rows:",
    find_duplicate_rows(df)
)

print(
    "Duplicate customer IDs:",
    find_duplicate_customer_ids(df)
)

print(
    "Invalid emails:",
    find_invalid_emails(df)
)

print(
    "Invalid ages:",
    find_invalid_ages(df)
)

print(
    "Invalid dates:",
    find_invalid_dates(df)
)

print(
    "Inconsistent countries:",
    find_inconsistent_countries(df)
)

print(
    "Invalid statuses:",
    find_invalid_statuses(df)
)

print(
    "Missing emails:",
    find_missing_emails(df)
)

print(
    "Missing phones:",
    find_missing_phones(df)
)

print(
    "Missing income:",
    find_missing_income(df)
)

print("\n--- COLUMN QUALITY ---")

for result in get_column_quality(df):
    print(
        f"{result['column']}: "
        f"{result['completeness']}% complete"
    )