def calculate_completeness(df):
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()

    if total_cells == 0:
        return 100.0

    score = ((total_cells - missing_cells) / total_cells) * 100

    return round(score, 2)


def calculate_uniqueness(df):
    total_rows = len(df)

    if total_rows == 0:
        return 100.0

    duplicate_rows = df.duplicated().sum()

    score = ((total_rows - duplicate_rows) / total_rows) * 100

    return round(score, 2)


def calculate_validity(
    invalid_emails,
    invalid_ages,
    invalid_dates,
    invalid_countries,
    invalid_statuses,
    total_rows
):
    if total_rows == 0:
        return 100.0

    total_issues = (
        invalid_emails
        + invalid_ages
        + invalid_dates
        + invalid_countries
        + invalid_statuses
    )

    issue_rate = total_issues / total_rows

    score = max(0, 100 - (issue_rate * 100))

    return round(score, 2)


def calculate_consistency(
    inconsistent_countries,
    total_rows
):
    if total_rows == 0:
        return 100.0

    issue_rate = inconsistent_countries / total_rows

    score = max(0, 100 - (issue_rate * 100))

    return round(score, 2)


def calculate_overall_score(
    completeness,
    validity,
    uniqueness,
    consistency
):
    score = (
        completeness * 0.30
        + validity * 0.30
        + uniqueness * 0.20
        + consistency * 0.20
    )

    return round(score, 2)