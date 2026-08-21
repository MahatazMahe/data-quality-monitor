import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


random.seed(42)

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

first_names = [
    "Rahim", "Karim", "Ahmed", "Hasan", "Tanvir",
    "Sarah", "Emily", "John", "Michael", "Maria",
    "David", "James", "Ayesha", "Nusrat", "Fatima"
]

last_names = [
    "Khan", "Rahman", "Ahmed", "Hossain", "Islam",
    "Smith", "Johnson", "Williams", "Brown", "Garcia"
]

countries = [
    "Bangladesh",
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Germany"
]

statuses = [
    "Active",
    "Inactive",
    "Suspended"
]


def random_date():
    start = datetime(2022, 1, 1)
    end = datetime(2026, 8, 1)
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def generate_customer(customer_id):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    return {
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{first_name.lower()}.{last_name.lower()}{customer_id}@example.com",
        "phone": f"+8801{random.randint(300000000, 999999999)}",
        "country": random.choice(countries),
        "signup_date": random_date().strftime("%Y-%m-%d"),
        "age": random.randint(18, 70),
        "annual_income": random.randint(20000, 150000),
        "customer_status": random.choice(statuses)
    }


customers = []

for customer_id in range(10001, 22501):
    customers.append(generate_customer(customer_id))


df = pd.DataFrame(customers)


# Introduce missing values
for index in random.sample(range(len(df)), 180):
    df.loc[index, "email"] = None

for index in random.sample(range(len(df)), 120):
    df.loc[index, "phone"] = None

for index in random.sample(range(len(df)), 100):
    df.loc[index, "annual_income"] = None


# Introduce invalid emails
for index in random.sample(range(len(df)), 100):
    df.loc[index, "email"] = "invalid-email"


# Introduce invalid ages
for index in random.sample(range(len(df)), 60):
    df.loc[index, "age"] = random.choice([-5, 0, 121, 150])


# Introduce inconsistent countries
for index in random.sample(range(len(df)), 80):
    df.loc[index, "country"] = random.choice([
        "BD",
        "USA",
        "UK",
        "United States ",
        "bangladesh"
    ])


# Introduce invalid dates
for index in random.sample(range(len(df)), 50):
    df.loc[index, "signup_date"] = random.choice([
        "not-a-date",
        "2026/99/99",
        "31-31-2025"
    ])


# Introduce duplicate customer IDs
duplicate_rows = df.sample(100, random_state=42).copy()
df = pd.concat([df, duplicate_rows], ignore_index=True)


# Shuffle the dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)


output_file = output_dir / "customers.csv"
df.to_csv(output_file, index=False)


print(f"Dataset created: {output_file}")
print(f"Total records: {len(df):,}")
print(f"Total columns: {len(df.columns)}")