# AI Coding Agent Instructions for Luigi Data Pipelines

## Architecture Overview

This is a **Luigi-based ETL orchestration system** that integrates multiple data sources and processing patterns:

- **Core Framework**: Luigi for workflow orchestration with dependency management
- **Data Sources**: Google Sheets API, web scraping (Scrapy), browser automation (Selenium)
- **Scheduling**: Custom APScheduler + file watchers for event-driven processing
- **Output**: CSV/Excel/PDF reports, NDJSON for scraped data, REST API (FastAPI)
- **Data Flow**: Extract → Transform (Pandas) → Load with automatic retries and logging

## Essential Patterns & Conventions

### Task Structure
```python
class MyTask(luigi.Task):
    date = luigi.DateParameter(default=datetime.now().date())
    sheet_id = luigi.Parameter(default="your_sheet_id")

    def requires(self):
        return [DependencyTask(date=self.date)]

    def output(self):
        return luigi.LocalTarget(OUTPUT_DATA_PATH / f"output_{self.date}.csv")

    def run(self):
        # Extract
        data = self._extract_data()
        # Transform
        df = self._transform_data(data)
        # Load
        df.to_csv(self.output().path, index=False)
```

### Logging & Error Handling
```python
import logging
logger = logging.getLogger("luigi-interface")
logger.info("Task starting...")

# Event handlers auto-registered in base_task.py
# SUCCESS, FAILURE, START events logged automatically
```

### Data Path Structure
```
data/
├── raw/          # Raw scraped data (NDJSON, HTML)
├── processed/    # Cleaned/transformed data
├── outputs/      # Final deliverables (CSV, Excel, PDF)
└── reports/      # Generated reports
```

## Critical Commands & Workflows

### Environment Setup
```bash
# Always use virtual environment
conda run -n luigi luigi --module ...
uv run python -m your_project.tasks.ExampleTask
```

### Running Tasks
```bash
# With central scheduler (production)
luigi --module your_project.tasks YourTaskName --scheduler-url http://localhost:8082

# Debug mode (local scheduler)
luigi --module ... --local-scheduler

# Custom scheduler (background service)
uv run python -m your_project.scheduler
```

### Scheduler Management
- **Central Scheduler**: Runs on port 8082, web UI at `http://localhost:8082`
- **Start Service**: Use VS Code task "Luigi: Start Scheduler (luigid)"
- **Custom Schedules**: Defined in `scheduler/schedules.yaml` with cron expressions

### File Watcher Integration
- Monitors folders for new files
- Auto-triggers tasks on file creation/modification
- Configured in `schedules.yaml` under `file_watchers`

## Integration Points

### Web Scraping (Scrapy)
- Spiders in `spiders/` directory
- Login handling with form submissions
- Output: NDJSON format in `data/outputs/scraped/`

### Browser Automation (Selenium)
- Used for complex web interactions
- ChromeDriver in `bin/chrome-win32/`
- Integrated with Luigi tasks via subprocess calls

### Email Notifications
- SMTP configured in `luigi.cfg`
- Automatic failure notifications
- Report attachments for hourly summaries

## Common Patterns

### Date Handling
```python
# Luigi DateParameter
date = luigi.DateParameter(default=datetime.now().date())

# Date formatting for APIs
date_str = self.date.strftime("%d/%m/%Y")
```

### DataFrame Operations
```python
# Filter null values
df = df[df['column'].notnull()]

# Add metadata columns
df['export_date'] = datetime.now()
df['source'] = 'sheet_name'
```

### Error Recovery
- Tasks are **idempotent** - safe to re-run
- `retry-count=3` in `luigi.cfg`
- Temporary paths for atomic writes: `self.output().temporary_path()`

### Parameter Patterns
```python
# Required parameters
sheet_id = luigi.Parameter()  # No default

# Optional with defaults
worksheet_name = luigi.Parameter(default="MES_ATUAL")
output_prefix = luigi.Parameter(default="DATA_TYPE")
```

## File Organization Reference

- `tasks/`: Luigi tasks for data processing
- `spiders/`: Scrapy spiders for web scraping
- `scrapers/`: Generic web scrapers
- `scheduler/`: Custom scheduling logic
- `api/`: FastAPI REST endpoints
- `bin/`: binaries, chromedriver and chrome binaries - good so we dont need to update it

## Testing & Validation

- Run individual tasks with `--local-scheduler` for debugging
- Check `logs/` directory for execution logs
- Use Luigi web UI to visualize dependency graphs
- Validate outputs in `data/outputs/` directory

## Key Files to Reference

- `luigi.cfg`: Luigi configuration
- `settings.py`: Path and Scrapy configurations
- `schedules.yaml`: Task scheduling definitions
- `tasks/core/base_task.py`: Event handlers and logging
- `tasks/core/extract_base.py`: Base extraction logic
- `README.md`: Project documentation and usage instructions