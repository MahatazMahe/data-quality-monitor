import sqlite3

from src.data_quality.database import DATABASE_PATH


connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


print("\n--- DATASETS ---")

cursor.execute("""
    SELECT *
    FROM datasets
""")

for row in cursor.fetchall():
    print(row)


print("\n--- QUALITY RUNS ---")

cursor.execute("""
    SELECT *
    FROM quality_runs
""")

for row in cursor.fetchall():
    print(row)


print("\n--- QUALITY METRICS ---")

cursor.execute("""
    SELECT
        metric_name,
        metric_value
    FROM quality_metrics
""")

for row in cursor.fetchall():
    print(row)


print("\n--- QUALITY ISSUES ---")

cursor.execute("""
    SELECT
        column_name,
        issue_type,
        issue_count,
        severity
    FROM quality_issues
    ORDER BY issue_count DESC
""")

for row in cursor.fetchall():
    print(row)


connection.close()