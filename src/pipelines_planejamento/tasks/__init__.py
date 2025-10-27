"""
Tasks package initialization

Imports base_task to ensure event handlers are registered before any task execution.
"""

# Import base_task first to register Luigi event handlers globally
try:
    from pipelines_planejamento.tasks.core import base_task
except Exception:
    import logging

    logging.getLogger("luigi-interface").exception(
        "Failed to import base_task and register event handlers"
    )


from .example_task import ExampleTask
from .run_spiders import RunPropostaSpiderTask

__all__ = ["ExampleTask", "RunPropostaSpiderTask"]
