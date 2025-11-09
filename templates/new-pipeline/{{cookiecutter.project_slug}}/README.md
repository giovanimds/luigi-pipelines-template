# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## 📋 Overview

This is a Luigi-based data pipeline project created using Cookiecutter templates.

**Author:** {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

## 🚀 Getting Started

### Prerequisites

- Python {{ cookiecutter.python_version }} or higher
- uv (Python package manager)

### Installation

1. **Create and activate a virtual environment**

```bash
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
uv sync
# OR
uv pip install -e .
```

3. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your configurations
```

## 🏃 Running the Pipeline

### Run a task locally

```bash
luigi --module {{ cookiecutter.project_slug }}.tasks ExampleTask --local-scheduler
```

### Start Luigi central scheduler

```bash
luigid --port 8082
```

{% if cookiecutter.include_scheduler == "y" %}### Start custom scheduler

```bash
python -m {{ cookiecutter.project_slug }}.scheduler
```
{% endif %}

{% if cookiecutter.include_scrapy == "y" %}### Run Scrapy spiders

```bash
scrapy crawl my_spider
```
{% endif %}

{% if cookiecutter.include_fastapi == "y" %}### Start API server

```bash
uvicorn {{ cookiecutter.project_slug }}.api.serve:app --reload
```
{% endif %}

## 📁 Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/{{ cookiecutter.project_slug }}/
│   ├── tasks/              # Luigi tasks
│   │   ├── core/           # Core task classes
│   │   └── ...
{% if cookiecutter.include_scrapy == "y" %}│   ├── spiders/            # Scrapy spiders
│   ├── scrapers/           # Custom scrapers
{% endif %}{% if cookiecutter.include_scheduler == "y" %}│   ├── scheduler/          # Task scheduling
{% endif %}{% if cookiecutter.include_fastapi == "y" %}│   ├── api/                # FastAPI endpoints
{% endif %}│   ├── utils/              # Utility functions
│   └── settings.py         # Configuration
├── data/
│   ├── raw/                # Raw data
│   ├── processed/          # Processed data
│   └── outputs/            # Final outputs
├── tests/                  # Unit tests
├── logs/                   # Application logs
├── pyproject.toml          # Project configuration
{% if cookiecutter.include_scrapy == "y" %}├── scrapy.cfg              # Scrapy configuration
{% endif %}└── README.md               # This file
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

## 📝 License

This project is licensed under the {{ cookiecutter.license }} License.
