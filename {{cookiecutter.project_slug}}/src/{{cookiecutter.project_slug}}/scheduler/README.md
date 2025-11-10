Luigi lightweight scheduler (Windows-friendly)

This folder contains a small APScheduler-based scheduler that can dispatch Luigi tasks on a schedule.

Files:

- luigi_scheduler.py - main scheduler service script (uses schedules.yaml)
- schedules.yaml - example schedule definitions (cron-like)

How it works:

- The scheduler reads `schedules.yaml` and creates APScheduler cron jobs.
- Each job executes `python -m luigi --module <module> <Task>` using the same Python interpreter running the script.
- The script passes the `--scheduler-host localhost --scheduler-port 8082` flags so that tasks are submitted to the central luigid.

Deployment suggestions (Windows):

- Run the script in the project Conda environment.
- Use Task Scheduler to start the script at system boot, or use NSSM to create a service wrapper.

Notes:

- Make sure `pyyaml` and `apscheduler` are installed in the environment.
- The scheduler runs jobs with the Python executable that started it; ensure that environment has access to your project and dependencies.
