# Data Quality Monitoring Dashboard

An interactive data quality monitoring system built with Python, SQLite, Pandas, Plotly, and Streamlit.

## Live Dashboard

**Coming soon**

## Overview

This project simulates a production-style data quality monitoring workflow for a customer dataset.

The system loads raw customer data, validates it against data quality rules, calculates quality metrics, stores historical pipeline results in SQLite, and exposes the results through an interactive monitoring dashboard.

## Architecture

```text
Raw Customer CSV
       ↓
Python Data Quality Pipeline
       ↓
Validation & Quality Checks
       ↓
Quality Metrics
       ↓
SQLite Database
       ↓
Interactive Streamlit Dashboard

Quality Dimensions

The pipeline evaluates four core data quality dimensions:

Completeness — measures missing data
Validity — identifies invalid values and formats
Uniqueness — detects duplicate records and customer IDs
Consistency — identifies inconsistent categorical values
Dashboard Features
Overall data quality score
Quality dimension analysis
Historical quality monitoring
Issue severity visualization
Column-level completeness analysis
Interactive quality run selection
Severity filtering
Column filtering
Issue search
Dataset preview
Filtered issue export
Historical pipeline results
Data Quality Checks

The pipeline detects:

Missing values
Missing emails
Missing phone numbers
Missing income
Duplicate records
Duplicate customer IDs
Invalid email addresses
Invalid ages
Invalid dates
Inconsistent country names
Current Dataset

The project uses synthetic customer data containing:

Field	Description
customer_id	Unique customer identifier
first_name	Customer first name
last_name	Customer last name
email	Customer email
phone	Customer phone number
country	Customer country
signup_date	Customer registration date
age	Customer age
annual_income	Annual customer income
customer_status	Customer account status

The dataset intentionally contains controlled data quality problems so that the monitoring pipeline has realistic issues to detect.

Example Pipeline Results

Current pipeline results:

Metric	Score
Overall Quality	98.91%
Completeness	99.68%
Validity	97.65%
Uniqueness	99.21%
Consistency	99.35%

Detected issues:

Issue	Count
Missing Values	402
Missing Email	182
Missing Phone	120
Invalid Email	103
Missing Income	100
Duplicate Customer ID	100
Duplicate Rows	100
Inconsistent Country	82
Invalid Age	61
Invalid Date	50
Technology Stack
Python
Pandas
SQLite
Plotly
Streamlit
Git
GitHub

Project Structure:

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

Running Locally
1. Clone the repository

git clone https://github.com/MahatazMahe/data-quality-monitor.git

cd data-quality-monitor

2. Create a virtual environment

python -m venv .venv

3. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Run the data quality pipeline
python pipeline.py
6. Launch the dashboard
streamlit run dashboard/app.py

The dashboard will be available at:

http://localhost:8501

Data Pipeline

The pipeline follows this workflow:

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

Each pipeline execution is recorded as a separate quality run, allowing historical monitoring of data quality.

Purpose

This project was built as a practical Data Engineering portfolio project to demonstrate:

Data validation
Data quality monitoring
Python data processing
SQL database persistence
Quality metric calculation
Interactive data visualization
Pipeline development
Dashboard development
Git and GitHub workflow
Author

Mahataz Mahe
Data Engineering Portfolio Project