import pandas as pd

df = pd.read_csv("data/raw/customers.csv")

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMNS ---")
print(df.columns.tolist())

print("\n--- FIRST 10 ROWS ---")
print(df.head(10).to_string(index=False))

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- UNIQUE CUSTOMER IDs ---")
print(df["customer_id"].nunique())

print("\n--- CUSTOMER STATUS ---")
print(df["customer_status"].value_counts())

print("\n--- COUNTRIES ---")
print(df["country"].value_counts())

print("\n--- AGE RANGE ---")
print(f"Minimum age: {df['age'].min()}")
print(f"Maximum age: {df['age'].max()}")

print("\n--- INVALID EMAIL EXAMPLES ---")
invalid_emails = df[
    ~df["email"].fillna("").str.contains("@", regex=False)
]

print(invalid_emails[["customer_id", "email"]].head(10).to_string(index=False))