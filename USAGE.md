# Using This Template

This repository is a Cookiecutter template for creating new Luigi data pipeline projects.

## Quick Start

### 1. Install Cookiecutter

```bash
pip install cookiecutter
```

### 2. Generate a New Project

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template
```

Or from a local clone:

```bash
cookiecutter /path/to/luigi-pipelines-template
```

### 3. Answer the Prompts

The template will ask you several questions to customize your project:

```
project_name [My Data Pipeline]: Sales Analytics Pipeline
project_slug [sales_analytics_pipeline]: 
project_short_description [Luigi-based data pipeline for ETL operations]: 
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
python_version [3.12]: 
version [0.1.0]: 
Select open_source_license:
1 - MIT
2 - Apache-2.0
3 - BSD-3-Clause
4 - GPL-3.0
5 - Proprietary
Choose from 1, 2, 3, 4, 5 [1]: 
include_scrapy [y]: 
include_fastapi [y]: 
include_scheduler [y]: 
```

### 4. Start Using Your New Project

```bash
cd sales_analytics_pipeline
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -e .
cp .env.example .env
cp luigi.cfg.example luigi.cfg
```

## Configuration Options

| Option | Description | Default | Options |
|--------|-------------|---------|---------|
| `project_name` | Display name for your project | My Data Pipeline | Any string |
| `project_slug` | Python package name | (auto-generated) | Valid Python identifier |
| `project_short_description` | Brief description | Luigi-based data pipeline... | Any string |
| `author_name` | Your full name | Your Name | Any string |
| `author_email` | Your email address | your.email@example.com | Valid email |
| `python_version` | Minimum Python version | 3.12 | 3.10, 3.11, 3.12+ |
| `version` | Initial version number | 0.1.0 | Semantic version |
| `open_source_license` | License for your project | MIT | MIT, Apache-2.0, BSD-3-Clause, GPL-3.0, Proprietary |
| `include_scrapy` | Include web scraping? | y | y/n |
| `include_fastapi` | Include REST API? | y | y/n |
| `include_scheduler` | Include task scheduler? | y | y/n |

## What You Get

### Always Included

- **Luigi** for workflow orchestration
- **Example tasks** showing common patterns
- **Configuration files** (.env, luigi.cfg)
- **Test structure** with pytest
- **Documentation** customized for your project

### Optional Components

#### Scrapy (include_scrapy=y)
- Web scraping framework
- Example spider
- Scrapy configuration
- Scrapy-specific dependencies

#### FastAPI (include_fastapi=y)
- REST API framework
- Example endpoints
- API server setup
- FastAPI dependencies

#### Scheduler (include_scheduler=y)
- APScheduler integration
- YAML-based scheduling
- File watchers
- Cron-like task scheduling

## Project Structure

```
your_project_slug/
├── src/
│   └── your_project_slug/
│       ├── tasks/          # Luigi tasks
│       ├── spiders/        # Scrapy spiders (if included)
│       ├── api/            # FastAPI endpoints (if included)
│       ├── scheduler/      # Task scheduling (if included)
│       ├── utils/          # Utility functions
│       └── settings.py     # Configuration
├── tests/                  # Unit tests
├── data/                   # Data directories
│   ├── raw/
│   ├── processed/
│   └── outputs/
├── logs/                   # Application logs
├── pyproject.toml          # Project configuration
└── README.md               # Project documentation
```

## Examples

### Minimal Project (Luigi only)

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template \
  --no-input \
  project_name="Simple Pipeline" \
  include_scrapy=n \
  include_fastapi=n \
  include_scheduler=n
```

### Full-Featured Project

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template \
  --no-input \
  project_name="Complete Pipeline" \
  include_scrapy=y \
  include_fastapi=y \
  include_scheduler=y
```

### Web Scraping Pipeline

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template \
  --no-input \
  project_name="Scraping Pipeline" \
  include_scrapy=y \
  include_fastapi=n \
  include_scheduler=y
```

## Post-Generation

After your project is generated, the post-generation hook will:

1. Remove components you didn't select
2. Clean up unused files
3. Display next steps

## Troubleshooting

### Template Not Found

If you get "template not found", try the full URL:

```bash
cookiecutter https://github.com/giovanimds/luigi-pipelines-template
```

### Permission Errors

Make sure you have write permissions in the directory where you're generating the project.

### Import Errors in Generated Project

After generating, make sure to:

1. Activate your virtual environment
2. Install the project: `pip install -e .`
3. Check that all dependencies are installed

## Support

- **Issues**: https://github.com/giovanimds/luigi-pipelines-template/issues
- **Discussions**: https://github.com/giovanimds/luigi-pipelines-template/discussions

## Contributing

To contribute to this template:

1. Fork the repository
2. Make changes in the `{{cookiecutter.project_slug}}/` directory
3. Test your changes: `cookiecutter .`
4. Submit a pull request

## License

The template itself is MIT licensed. Generated projects can use any license selected during generation.
