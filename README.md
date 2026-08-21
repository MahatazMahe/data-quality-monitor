# Data Quality Monitoring Dashboard

An interactive data quality monitoring system that validates a customer dataset, calculates quality metrics, tracks results over time, and surfaces everything through a Streamlit dashboard.

Built with **Python, Pandas, SQLite, Plotly, and Streamlit**.

---

## Overview

Most data pipelines fail quietly — a missing field here, a duplicate record there — and by the time it shows up in a report, it's hard to trace back to the source. This project simulates a production-style data quality workflow to address that: it loads raw customer data, runs it through a set of validation rules, scores it across multiple quality dimensions, and stores every run so quality can be tracked over time rather than checked once and forgotten.

**Pipeline flow:**

```
Raw Customer CSV
      ↓
Data Quality Pipeline (Python)
      ↓
Validation & Quality Checks
      ↓
Quality Metrics
      ↓
SQLite Database
      ↓
Streamlit Dashboard
```

---

## Quality Dimensions

The pipeline evaluates data across four core dimensions:

| Dimension | What it measures |
|---|---|
| **Completeness** | Missing data across required fields |
| **Validity** | Invalid values and malformed formats |
| **Uniqueness** | Duplicate records and duplicate customer IDs |
| **Consistency** | Inconsistent categorical values (e.g. country names) |

---

## What It Checks

- Missing values (overall, plus email / phone / income specifically)
- Duplicate records and duplicate customer IDs
- Invalid email addresses
- Invalid ages
- Invalid dates
- Inconsistent country naming

---

## Dashboard Features

- Overall data quality score
- Per-dimension quality breakdown
- Historical quality tracking across pipeline runs
- Issue severity visualization
- Column-level completeness analysis
- Run selection, severity filtering, and column filtering
- Issue search
- Dataset preview
- Filtered issue export

---

## Dataset

The pipeline runs against a synthetic customer dataset with the following fields:

| Field | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `first_name` | Customer first name |
| `last_name` | Customer last name |
| `email` | Customer email |
| `phone` | Customer phone number |
| `country` | Customer country |
| `signup_date` | Customer registration date |
| `age` | Customer age |
| `annual_income` | Annual customer income |
| `customer_status` | Customer account status |

The dataset intentionally includes controlled data quality issues so the pipeline has realistic problems to detect and score.

---

## Example Pipeline Results

**Quality scores:**

| Metric | Score |
|---|---|
| Overall Quality | 98.91% |
| Completeness | 99.68% |
| Validity | 97.65% |
| Uniqueness | 99.21% |
| Consistency | 99.35% |

**Issues detected:**

| Issue | Count |
|---|---|
| Missing Values | 402 |
| Missing Email | 182 |
| Missing Phone | 120 |
| Invalid Email | 103 |
| Missing Income | 100 |
| Duplicate Customer ID | 100 |
| Duplicate Rows | 100 |
| Inconsistent Country | 82 |
| Invalid Age | 61 |
| Invalid Date | 50 |

---

## Tech Stack

- **Python** — pipeline and validation logic
- **Pandas** — data processing
- **SQLite** — persistence of quality runs and issues
- **Plotly** — visualizations
- **Streamlit** — dashboard interface
- **Git / GitHub** — version control

---

## Project Structure

```
data-quality-monitor/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── customers.csv
│   └── quality.db
│
├── src/
│   └── data_quality/
│       ├── database.py
│       ├── metrics.py
│       └── validators.py
│
├── .streamlit/
│   └── config.toml
│
├── generate_data.py
├── inspect_data.py
├── test_quality.py
├── calculate_score.py
├── pipeline.py
├── initialize_database.py
├── inspect_database.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running Locally

**1. Clone the repository**

```bash
git clone https://github.com/MahatazMahe/data-quality-monitor.git
cd data-quality-monitor
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the virtual environment**

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the data quality pipeline**

```bash
python pipeline.py
```

**6. Launch the dashboard**

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at `http://localhost:8501`.

---

## Data Pipeline

```
Customer Dataset
      ↓
Load Data
      ↓
Run Validation Rules
      ↓
Calculate Quality Metrics
      ↓
Calculate Overall Score
      ↓
Store Results in SQLite
      ↓
Record Quality Issues
      ↓
Dashboard
```

Each pipeline execution is stored as a distinct quality run, which is what enables historical tracking rather than a single point-in-time check.

---

## Purpose

This was built as a Data Engineering portfolio project to get hands-on practice with the full lifecycle of a data quality workflow — not just writing validation rules, but structuring a pipeline, persisting results in a queryable form, and turning raw checks into metrics that are actually usable for monitoring over time. It covers:

- Data validation
- Data quality monitoring
- Python data processing
- SQL-based persistence
- Quality metric calculation
- Interactive data visualization
- Pipeline development
- Dashboard development
- Git/GitHub workflow

---

## Author

**Mahataz Mahe**
CS/CSE undergraduate building toward a career in Data Engineering.
Data Engineering Portfolio Project
