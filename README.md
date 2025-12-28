# Code Quality Assessment Tool

## Description
Code Quality Assessment Tool is a Python project that automatically evaluates the quality of student Python code using a set of measurable metrics and produces a final grade with recommendations.

The tool generates reports in two formats:
- JSON (machine-readable).
- Markdown (human-readable).

## Installation

### Prerequisites
- Python 3.8+ (recommended: Python 3.10).
- pip (or conda).

### Setup
```
git clone <repo-url>
cd <project-name>

python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

### Input data format
Put student submissions into a single folder, where each student has their own subfolder:

```
data/student_submissions/
  student_001/
    ...
  student_002/
    ...
```

### Basic Example
Run analysis for all student folders and generate both reports:

```
python -m src.main --input data/student_submissions --out out
```

Output files:
- `out/report.json`
- `out/report.md`

### Advanced Usage
Optional examples (implement flags as the project evolves):

```
python -m src.main --input data/student_submissions --out out --fail-under 60
python -m src.main --input data/student_submissions --out out --format json
```

## Project Structure
```
.
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py               # CLI entrypoint
│   ├── scoring.py            # Scoring rules: metrics -> grade + recommendations
│   ├── report.py             # JSON/Markdown report generation
│   └── metrics/              # Independent metric calculators
├── tests/                    # Unit tests
│   ├── __init__.py
│   └── test_*.py
├── data/                     # Sample data (small examples only)
│   └── student_submissions/  # Sample student projects
├── docs/                     # Documentation (optional)
├── scripts/                  # Utility scripts (optional)
├── .github/workflows/        # CI/CD workflows
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements
All dependencies are listed in `requirements.txt`.

Recommended minimum set (extend as needed):
- Testing: `pytest`, `pytest-cov`
- Code quality: `flake8`, `black`

## Testing
Run unit tests:

```
pytest
```

Run tests with coverage:

```
pytest --cov=src tests
```

## CI/CD
This repository is intended to be used with GitHub/GitVerse Actions workflows:
- On every push/pull request: run linting (PEP 8), formatting checks, and unit tests.
- Optionally: run a scheduled workflow (`cron`) or a manual workflow (`workflow_dispatch`) that generates reports and uploads them as artifacts.

![Tests and Code Quality](https://github.com/akogarechau/final_project_itis/actions/workflows/tests.yml/badge.svg)

## Contributing
- Create a feature branch.
- Add/update unit tests for new functionality.
- Ensure CI passes (lint + tests) before opening a PR.

## License


## Author
Timur Sotnik (URFU/ITIS)
