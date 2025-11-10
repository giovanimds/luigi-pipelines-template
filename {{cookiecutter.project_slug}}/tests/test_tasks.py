"""
Unit tests for Luigi tasks

Run with: pytest tests/
"""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from pipelines_planejamento.tasks import ExampleTask


class TestExtractDataTask:
    """Tests for ExtractDataTask"""
    
    def test_task_creation(self):
        """Test task can be created"""
        task = ExampleTask(date=date(2025, 10, 1), source="test")
        assert task.date == date(2025, 10, 1)
    
    def test_output_path(self):
        """Test output path is correct"""
        task = ExampleTask(date=date(2025, 10, 1), source="test")
        output = task.output()[0]
        assert "raw_data_test_2025-10-01.csv" in str(output.path)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
