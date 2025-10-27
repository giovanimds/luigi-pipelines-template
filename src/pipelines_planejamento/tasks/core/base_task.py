
import logging
import luigi

# Você pode importar esse arquivo para definir o tratamento de eventos das tasks

@luigi.Task.event_handler(luigi.Event.FAILURE)
def fail_handler(task, exception):
    logger = logging.getLogger("luigi-interface")
    logger.error(f"Task {task} failed with exception: {exception}")
    # Additional failure handling logic can be added here


@luigi.Task.event_handler(luigi.Event.SUCCESS)
def success_handler(task):
    logger = logging.getLogger("luigi-interface")
    logger.info(f"Task {task} completed successfully")
    # Additional success handling logic can be added here


@luigi.Task.event_handler(luigi.Event.START)
def start_handler(task):
    logger = logging.getLogger("luigi-interface")
    logger.info(f"Task {task} is starting")
    # Additional start handling logic can be added here


@luigi.Task.event_handler(luigi.Event.BROKEN_TASK)
def broken_handler(task, *args, **kwargs):
    logger = logging.getLogger("luigi-interface")
    logger.error(f"Task {task} marked as BROKEN. args={args} kwargs={kwargs}")


@luigi.Task.event_handler(luigi.Event.PROCESS_FAILURE)
def process_failure_handler(task, exception):
    logger = logging.getLogger("luigi-interface")
    logger.error(f"Task {task} failed during processing with exception: {exception}")
    # Additional process failure handling logic can be added here
