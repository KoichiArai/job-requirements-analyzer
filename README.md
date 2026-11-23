# Job Requirements Analyzer

A Python CLI application that analyzes technology trends in job postings.

The application reads job posting data from a CSV file, validates and classifies each posting, extracts normalized technology keywords, stores the results in SQLite, and generates monthly comparison reports.

This project was created to analyze skill demand for QA Automation, SDET, Backend, and Web Developer roles in the Canadian technology job market.

## Features

- Reads job postings from CSV
- Validates required columns and values
- Validates collection dates in `YYYY-MM-DD` format
- Classifies job postings by role
- Extracts and normalizes technology keywords
- Prevents duplicate job records
- Stores job data in SQLite
- Generates keyword frequency reports
- Generates month-over-month comparison reports
- Writes execution logs to both the console and a log file
- Supports custom input and output paths through CLI arguments
- Includes automated tests with pytest
- Uses Ruff for linting and formatting

## Supported Role Categories

- SDET
- QA Automation
- QA / Software Testing
- Backend
- Web / Full Stack
- Others

## Example Technology Keywords

- Python
- Java
- JavaScript
- FastAPI
- PostgreSQL
- Redis
- Docker
- AWS
- Git
- GitHub Actions
- CI/CD
- pytest
- Selenium
- Playwright
- Jenkins
- REST API
- API Testing

## Requirements

- Python 3.12 or later

The project is currently tested locally with Python 3.14.

## Project Structure

```text
job-requirements-analyzer/
├── data/
│   └── sample.csv
├── tests/
│   ├── test_cli.py
│   ├── test_database.py
│   ├── test_date_validation.py
│   ├── test_job_classifier.py
│   ├── test_keyword_extractor.py
│   ├── test_logging_config.py
│   └── test_report_generator.py
├── database.py
├── job_classifier.py
├── keyword_extractor.py
├── logging_config.py
├── main.py
├── report_generator.py
├── pyproject.toml
├── .gitignore
└── README.md
```

The following directories and files are created during execution and are not committed to Git:

```text
data/job_market.db
logs/job_analyzer.log
reports/keyword_frequency.csv
reports/monthly_comparison.csv
```

## Installation

Clone the repository and move into the project directory.

```powershell
git clone <repository-url>
cd job-requirements-analyzer
```

Create and activate a virtual environment.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the application and development dependencies.

```powershell
python -m pip install -e ".[dev]"
```

## CSV Format

The input CSV must contain the following columns:

| Column | Description |
|---|---|
| `collected_at` | Collection date in `YYYY-MM-DD` format |
| `title` | Job title |
| `company` | Company name |
| `location` | Job location |
| `url` | Job posting URL |
| `description` | Job description |
| `requirements` | Required skills and qualifications |

Example:

```csv
collected_at,title,company,location,url,description,requirements
2026-10-01,QA Automation Engineer,Example Company,Toronto,https://example.com/jobs/1,Develop automated tests,Python Selenium REST API Git CI/CD
```

## Usage

Run the application using the default paths:

```powershell
python .\main.py
```

The default paths are:

```text
Input CSV: data/sample.csv
Database: data/job_market.db
Reports: reports/
Log file: logs/job_analyzer.log
```

Custom paths can also be specified:

```powershell
python .\main.py `
    --input .\data\sample.csv `
    --database .\data\job_market.db `
    --reports-dir .\reports `
    --log-file .\logs\job_analyzer.log
```

Display the available options:

```powershell
python .\main.py --help
```

## Generated Reports

### Keyword Frequency Report

```text
reports/keyword_frequency.csv
```

This report contains keyword counts grouped by month and role category.

### Monthly Comparison Report

```text
reports/monthly_comparison.csv
```

This report compares each keyword's job count with the previous available month.

Example:

```csv
month,previous_month,keyword,job_count,previous_job_count,change,change_percent
2026-10,2026-09,Python,3,2,1,50.0
2026-10,2026-09,pytest,1,0,1,
```

A blank `change_percent` means that the previous count was zero and a percentage could not be calculated.

## Testing

Run all automated tests:

```powershell
python -m pytest -v
```

## Linting and Formatting

Check the source code:

```powershell
python -m ruff check .
```

Check formatting:

```powershell
python -m ruff format --check .
```

Automatically fix supported lint issues:

```powershell
python -m ruff check . --fix
```

Format the source code:

```powershell
python -m ruff format .
```

## Data and Privacy

The repository contains only fictional sample job data.

Real job posting data, generated databases, reports, and log files should not be committed to the repository.

When collecting job posting data, users are responsible for following the applicable website terms of service, robots policies, privacy requirements, and access restrictions.

## Future Improvements

- Import JSON job data
- Add configurable keyword dictionaries
- Add role-specific trend comparisons
- Add GitHub Actions for automated tests and linting
- Migrate from SQLite to PostgreSQL
- Provide a REST API with FastAPI
- Containerize the application with Docker
- Add a dashboard for trend visualization