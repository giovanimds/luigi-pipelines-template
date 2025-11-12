"""
Lightweight cron-like scheduler for Luigi tasks using APScheduler.

Reads schedules from schedules.yaml and dispatches Luigi commands (python -m luigi ...)
pointing to the central `luigid` scheduler (default localhost:8082).

Run this script under the Python/Conda environment where your project is configured.
Use Windows Task Scheduler or NSSM to run it at startup for a service-like behavior.
"""

import fnmatch
import logging
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from watchdog.events import FileCreatedEvent, FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger("luigi-scheduler")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

MODULE_DIR = Path(__file__).resolve().parent
SCHEDULE_FILE = MODULE_DIR / "schedules.yaml"

print(SCHEDULE_FILE)

# Default scheduler host/port for luigid
SCHEDULER_HOST = "localhost"
SCHEDULER_PORT = "8082"


class FileWatcherHandler(FileSystemEventHandler):
    """Handler para eventos de file system que dispara tasks Luigi."""

    def __init__(self, scheduler, file_watcher_configs: List[Dict[str, Any]]):
        self.scheduler = scheduler
        self.file_watcher_configs = file_watcher_configs
        self.last_triggered = {}  # Para controle de cooldown por arquivo

    def on_modified(self, event):
        """Processa eventos de modificação de arquivo."""
        if event.is_directory:
            return

        # Encontra configurações que correspondem a este evento
        for watcher_config in self.file_watcher_configs:
            if self._should_process_event(event, watcher_config):
                self._trigger_task(event, watcher_config)
                break  # Processa apenas a primeira configuração que corresponder

    def _should_process_event(self, event, watcher_config: Dict[str, Any]) -> bool:
        """Verifica se o evento deve ser processado baseado na configuração."""
        # Verifica se o evento está na lista de eventos monitorados
        watched_events = watcher_config.get("events", ["created", "modified"])
        if not any(
            isinstance(
                event,
                getattr(
                    __import__(
                        "watchdog.events", fromlist=[f"File{evt_type.title()}Event"]
                    ),
                    f"File{evt_type.title()}Event",
                ),
            )
            for evt_type in watched_events
        ):
            return False

        # Verifica se o caminho do arquivo está dentro do diretório monitorado
        watch_path = Path(watcher_config["path"]).resolve()
        if not str(event.src_path).startswith(str(watch_path)):
            return False

        # Verifica padrões de arquivo
        file_name = Path(event.src_path).name
        patterns = watcher_config.get("patterns", ["*"])
        if not any(fnmatch.fnmatch(file_name, pattern) for pattern in patterns):
            return False

        # Verifica cooldown
        cooldown = watcher_config.get("cooldown", 0)
        if cooldown > 0:
            last_trigger = self.last_triggered.get(event.src_path, 0)
            if time.time() - last_trigger < cooldown:
                return False

        return True

    def _trigger_task(self, event, watcher_config: Dict[str, Any]):
        """Dispara a task Luigi correspondente."""
        task_config = watcher_config.get("task", {})
        if not task_config:
            logger.warning(
                f"No task configured for file watcher: {watcher_config.get('name')}"
            )
            return

        module = task_config.get("module")
        task_class = task_config.get("task_class")

        if not module or not task_class:
            logger.warning(
                f"Incomplete task configuration for file watcher: {watcher_config.get('name')}"
            )
            return

        # Extrai parâmetros do evento
        file_path = event.src_path
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix
        dir_path = str(Path(file_path).parent)

        # Substitui placeholders nos parâmetros
        params = watcher_config.get("params", {})
        processed_params = {}
        for key, value in params.items():
            if isinstance(value, str):
                processed_value = value.format(
                    file_path=file_path,
                    file_name=file_name,
                    file_ext=file_ext,
                    dir_path=dir_path,
                )
                processed_params[key] = processed_value
            else:
                processed_params[key] = value

        # Marca timestamp para cooldown
        self.last_triggered[file_path] = time.time()

        # Executa a task em background
        import threading

        thread = threading.Thread(
            target=self._run_luigi_task,
            args=(module, task_class, processed_params, file_path),
        )
        thread.daemon = True
        thread.start()

        logger.info(f"Triggered task {module}.{task_class} for file: {file_path}")

    def _run_luigi_task(
        self, module: str, task_class: str, params: Dict[str, Any], file_path: str
    ):
        """Executa a task Luigi em uma thread separada."""
        try:
            cmd = [
                sys.executable,
                "-m",
                "luigi",
                "--module",
                module,
                task_class,
                "--scheduler-host",
                SCHEDULER_HOST,
                "--scheduler-port",
                SCHEDULER_PORT,
            ]

            # Adiciona parâmetros
            for key, value in params.items():
                cmd.extend([f'--{key.replace("_", "-")}', str(value)])

            timestamp = datetime.now().isoformat()
            logger.info(
                f"[{timestamp}] Running Luigi task for file {file_path}: {' '.join(cmd)}"
            )

            completed = subprocess.run(cmd, capture_output=True, text=True)

            if completed.returncode != 0:
                error_msg = (
                    f"Luigi task FAILED for file {file_path}: {module}.{task_class}\n"
                    f"Exit code: {completed.returncode}\n"
                    f"Command: {' '.join(cmd)}\n"
                    f"--- stdout ---\n{completed.stdout}\n"
                    f"--- stderr ---\n{completed.stderr}"
                )
                logger.error(error_msg)
            else:
                logger.info(f"Luigi task completed successfully for file: {file_path}")

        except Exception as e:
            logger.exception(f"Failed to run Luigi task for file {file_path}: {e}")


def load_schedules(path: Path):
    if not path.exists():
        logger.error(f"Schedule file not found: {path}")
        return [], []
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("schedules", []), data.get("file_watchers", [])


def run_luigi_job(
    module: str, task: str, date_arg: Optional[str] = None, extra_args=None
):
    extra_args = extra_args or []
    cmd = [
        sys.executable,
        "-m",
        "luigi",
        "--module",
        module,
        task,
        "--scheduler-host",
        SCHEDULER_HOST,
        "--scheduler-port",
        SCHEDULER_PORT,
    ]
    if date_arg:
        cmd += ["--date", date_arg]
    cmd += extra_args

    timestamp = datetime.now().isoformat()
    logger.info(f"[{timestamp}] Running Luigi job: {' '.join(cmd)}")
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True)

        # Log stdout/stderr
        if completed.stdout:
            logger.info(f"Luigi stdout:\n{completed.stdout}")
        if completed.stderr:
            logger.info(f"Luigi stderr:\n{completed.stderr}")

        # Se o processo falhou (exit != 0), dispara ERROR para acionar o handler de email
        if completed.returncode != 0:
            error_msg = (
                f"Luigi job FAILED: {module}.{task}\n"
                f"Exit code: {completed.returncode}\n"
                f"Command: {' '.join(cmd)}\n"
                f"--- stdout ---\n{completed.stdout}\n"
                f"--- stderr ---\n{completed.stderr}"
            )
            logger.error(error_msg)
        else:
            logger.info(
                f"Luigi job completed successfully (exit {completed.returncode})"
            )

    except Exception as e:
        logger.exception(f"Failed to run Luigi job: {e}")


def create_job(sched: BlockingScheduler, entry: dict):
    name = entry.get("name")
    module = entry["module"]
    task = entry["task"]
    cron = entry["cron"]  # crontab-like string
    date_mode = entry.get("date_mode", "today")
    extra_args = entry.get("extra_args", [])
    params = entry.get("params", {})

    # Parse cron string (standard 5-field)
    trigger = CronTrigger.from_crontab(cron)

    def job_wrapper():
        # Determine date argument
        # Luigi expects ISO date format YYYY-MM-DD for DateParameter parsing.
        if date_mode == "today":
            date_arg = datetime.now().strftime("%Y-%m-%d")
        elif date_mode == "yesterday":
            date_arg = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_mode == "none":
            date_arg = None
        else:
            date_arg = datetime.now().strftime("%Y-%m-%d")

        # Build extra args from params
        # Support a dynamic token value '__current_hour__' which will be
        # replaced with the current hour formatted as 'HH00' (ex: '0900').
        param_args = []
        now = datetime.now()
        for key, value in params.items():
            v = value
            if isinstance(v, str) and v == "__current_hour__":
                v = f"{now.hour:02d}00"
            param_args.extend([f'--{key.replace("_", "-")}', str(v)])

        all_extra_args = extra_args + param_args
        run_luigi_job(module, task, date_arg=date_arg, extra_args=all_extra_args)

    sched.add_job(job_wrapper, trigger=trigger, id=name, name=name)
    logger.info(
        f"Scheduled job '{name}' cron='{cron}' -> {module}.{task} (date_mode={date_mode})"
    )


def main():
    schedules, file_watchers = load_schedules(SCHEDULE_FILE)
    if not schedules and not file_watchers:
        logger.error("No schedules or file watchers found. Exiting.")
        return

    sched = BlockingScheduler()

    # Schedule initial jobs
    for entry in schedules:
        try:
            create_job(sched, entry)
        except Exception:
            logger.exception(f"Failed to schedule entry: {entry}")

    # Setup file watchers
    file_observers = []
    
    # Setup schedule file watcher (detects changes to schedules.yaml)
    try:
        schedule_observer = _setup_schedule_watcher(sched)
        if schedule_observer:
            file_observers.append(schedule_observer)
    except Exception:
        logger.exception("Failed to setup schedule file watcher")
    
    # Setup task-specific file watchers
    if file_watchers:
        logger.info(f"Setting up {len(file_watchers)} file watcher(s)...")
        for watcher_config in file_watchers:
            try:
                observer = _setup_file_watcher(sched, watcher_config)
                if observer:
                    file_observers.append(observer)
            except Exception:
                logger.exception(
                    f"Failed to setup file watcher: {watcher_config.get('name', 'unknown')}"
                )

    def _handle_sig(signum, frame):
        logger.info("Shutting down scheduler...")
        sched.shutdown(wait=False)
        # Stop file observers
        for observer in file_observers:
            observer.stop()
        for observer in file_observers:
            observer.join()

    signal.signal(signal.SIGINT, _handle_sig)
    signal.signal(signal.SIGTERM, _handle_sig)

    logger.info("Starting scheduler...")
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


class ScheduleUpdateHandler(FileSystemEventHandler):
    """Handler específico para detectar mudanças em schedules.yaml."""

    def __init__(self, scheduler: BlockingScheduler):
        self.scheduler = scheduler

    def on_modified(self, event):
        """Processa mudanças no schedules.yaml."""
        if event.is_directory:
            return

        file_path = Path(str(event.src_path))
        if file_path.name != "schedules.yaml":
            return

        logger.info(
            f"Detected change in {file_path.name}. Updating scheduled jobs..."
        )
        self._update_schedules()

    def _update_schedules(self):
        """Recarrega e reschedula os jobs."""
        try:
            new_schedules, _ = load_schedules(SCHEDULE_FILE)
            if not new_schedules:
                logger.warning("No schedules found in updated schedule file.")
                return

            # Remove all existing scheduled cron jobs (mantém observers/watchers)
            for job in list(self.scheduler.get_jobs()):
                self.scheduler.remove_job(job.id)

            # Reschedule jobs from updated file
            for entry in new_schedules:
                try:
                    create_job(self.scheduler, entry)
                except Exception:
                    logger.exception(f"Failed to schedule entry: {entry}")

            logger.info("Rescheduled jobs from updated schedule file.")
        except Exception as e:
            logger.exception(f"Error while updating schedules: {e}")


def _setup_file_watcher(
    sched: BlockingScheduler, watcher_config: Dict[str, Any]
):
    """Configura um file watcher baseado na configuração."""
    name = watcher_config.get("name", "unnamed")
    watch_path = watcher_config.get("path")

    if not watch_path:
        logger.error(f"File watcher '{name}' missing 'path' configuration")
        return None

    # Converte para Path absoluto
    watch_path = Path(watch_path).resolve()

    # Cria o diretório se não existir
    watch_path.mkdir(parents=True, exist_ok=True)

    # Cria o event handler
    event_handler = FileWatcherHandler(sched, [watcher_config])

    # Cria o observer
    observer = Observer()
    observer.schedule(
        event_handler, str(watch_path), recursive=watcher_config.get("recursive", False)
    )

    logger.info(f"File watcher '{name}' monitoring: {watch_path}")
    observer.start()

    return observer


def _setup_schedule_watcher(sched: BlockingScheduler):
    """Configura um file watcher para monitorar mudanças em schedules.yaml."""
    watch_path = SCHEDULE_FILE.parent

    event_handler = ScheduleUpdateHandler(sched)

    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)

    logger.info(f"Schedule file watcher monitoring: {watch_path}")
    observer.start()

    return observer


if __name__ == "__main__":
    main()
