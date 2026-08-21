import pandas as pd

from src.data_quality.metrics import (
    calculate_completeness,
    calculate_consistency,
    calculate_overall_score,
    calculate_uniqueness,
    calculate_validity,
)

from src.data_quality.validators import (
    find_inconsistent_countries,
    find_invalid_ages,
    find_invalid_dates,
    find_invalid_emails,
    find_invalid_statuses,
)


df = pd.read_csv("data/raw/customers.csv")

total_rows = len(df)

completeness = calculate_completeness(df)

uniqueness = calculate_uniqueness(df)

validity = calculate_validity(
    invalid_emails=find_invalid_emails(df),
    invalid_ages=find_invalid_ages(df),
    invalid_dates=find_invalid_dates(df),
    invalid_countries=find_inconsistent_countries(df),
    invalid_statuses=find_invalid_statuses(df),
    total_rows=total_rows,
)

consistency = calculate_consistency(
    inconsistent_countries=find_inconsistent_countries(df),
    total_rows=total_rows,
)

overall = calculate_overall_score(
    completeness=completeness,
    validity=validity,
    uniqueness=uniqueness,
    consistency=consistency,
)


print("\n--- DATA QUALITY SCORE ---")

print(f"Completeness : {completeness}%")
print(f"Validity     : {validity}%")
print(f"Uniqueness   : {uniqueness}%")
print(f"Consistency  : {consistency}%")
print(f"Overall      : {overall}%")