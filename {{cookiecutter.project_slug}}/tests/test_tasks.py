"""
Unit tests for Luigi tasks

Run with: pytest tests/
"""
from datetime import date

import pandas as pd
import pytest

from {{ cookiecutter.project_slug }}.tasks import ExampleTask


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
