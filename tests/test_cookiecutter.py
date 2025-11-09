"""
Unit tests for Cookiecutter template generation

Run with: pytest tests/test_cookiecutter.py -v
"""
import os
import shutil
import tempfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


# Get the project root and templates directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"


class TestCookiecutterTemplates:
    """Tests for Cookiecutter templates"""

    def test_luigi_task_template_exists(self):
        """Test that Luigi task template exists"""
        template_path = TEMPLATES_DIR / "luigi-task"
        assert template_path.exists(), f"Template not found at {template_path}"
        assert (template_path / "cookiecutter.json").exists()

    def test_scrapy_spider_template_exists(self):
        """Test that Scrapy spider template exists"""
        template_path = TEMPLATES_DIR / "scrapy-spider"
        assert template_path.exists(), f"Template not found at {template_path}"
        assert (template_path / "cookiecutter.json").exists()

    def test_new_pipeline_template_exists(self):
        """Test that new pipeline template exists"""
        template_path = TEMPLATES_DIR / "new-pipeline"
        assert template_path.exists(), f"Template not found at {template_path}"
        assert (template_path / "cookiecutter.json").exists()

    def test_generate_luigi_task(self):
        """Test generating a Luigi task from template"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = str(TEMPLATES_DIR / "luigi-task")
            
            # Generate task with default values
            result = cookiecutter(
                template_path,
                output_dir=tmpdir,
                no_input=True,
                extra_context={
                    "task_name": "TestGeneratedTask",
                    "task_description": "A test generated task",
                    "task_type": "basic",
                    "include_requires": "n",
                    "include_date_parameter": "y",
                    "output_format": "csv",
                    "author_name": "Test User",
                    "author_email": "test@test.com"
                }
            )
            
            # Verify task was created
            assert os.path.exists(result)
            task_file = Path(result) / "testgeneratedtask.py"
            assert task_file.exists(), f"Task file not found at {task_file}"
            
            # Verify content
            content = task_file.read_text()
            assert "class TestGeneratedTask" in content
            assert "A test generated task" in content
            assert "luigi.Task" in content

    def test_generate_scrapy_spider(self):
        """Test generating a Scrapy spider from template"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = str(TEMPLATES_DIR / "scrapy-spider")
            
            # Generate spider with default values
            result = cookiecutter(
                template_path,
                output_dir=tmpdir,
                no_input=True,
                extra_context={
                    "spider_name": "test_spider",
                    "spider_description": "A test spider",
                    "start_urls": "https://example.com",
                    "allowed_domains": "example.com",
                    "spider_type": "basic",
                    "include_login": "n",
                    "output_items": "title,url,description",
                    "author_name": "Test User",
                    "author_email": "test@test.com"
                }
            )
            
            # Verify spider was created
            assert os.path.exists(result)
            spider_file = Path(result) / "test_spider_spider.py"
            assert spider_file.exists(), f"Spider file not found at {spider_file}"
            
            # Verify content
            content = spider_file.read_text()
            assert "class Test_spiderSpider" in content
            assert "scrapy.Spider" in content
            assert "example.com" in content

    def test_generate_new_pipeline(self):
        """Test generating a new pipeline project from template"""
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = str(TEMPLATES_DIR / "new-pipeline")
            
            # Generate pipeline with default values
            result = cookiecutter(
                template_path,
                output_dir=tmpdir,
                no_input=True,
                extra_context={
                    "project_name": "Test Pipeline",
                    "project_slug": "test_pipeline",
                    "project_description": "A test pipeline project",
                    "author_name": "Test User",
                    "author_email": "test@test.com",
                    "python_version": "3.12",
                    "include_scrapy": "y",
                    "include_fastapi": "y",
                    "include_scheduler": "y",
                    "license": "MIT"
                }
            )
            
            # Verify project was created
            assert os.path.exists(result)
            readme_file = Path(result) / "README.md"
            assert readme_file.exists(), f"README file not found at {readme_file}"
            
            # Verify content
            content = readme_file.read_text()
            assert "Test Pipeline" in content
            assert "A test pipeline project" in content

    def test_task_template_with_different_types(self):
        """Test generating tasks with different types"""
        task_types = ["basic", "extract", "transform", "load"]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = str(TEMPLATES_DIR / "luigi-task")
            
            for task_type in task_types:
                # Generate task with specific type
                result = cookiecutter(
                    template_path,
                    output_dir=tmpdir,
                    no_input=True,
                    extra_context={
                        "task_name": f"Test{task_type.capitalize()}Task",
                        "task_description": f"Test {task_type} task",
                        "task_type": task_type,
                        "include_requires": "n",
                        "include_date_parameter": "y",
                        "output_format": "csv",
                        "author_name": "Test User",
                        "author_email": "test@test.com"
                    }
                )
                
                # Verify task was created with correct type
                assert os.path.exists(result)
                task_file = Path(result) / f"test{task_type}task.py"
                assert task_file.exists()
                
                content = task_file.read_text()
                assert f"class Test{task_type.capitalize()}Task" in content

    def test_task_template_output_formats(self):
        """Test generating tasks with different output formats"""
        output_formats = ["csv", "json", "excel", "parquet"]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = str(TEMPLATES_DIR / "luigi-task")
            
            for fmt in output_formats:
                # Generate task with specific format
                result = cookiecutter(
                    template_path,
                    output_dir=tmpdir,
                    no_input=True,
                    extra_context={
                        "task_name": f"Test{fmt.capitalize()}Task",
                        "task_description": f"Test {fmt} task",
                        "task_type": "basic",
                        "include_requires": "n",
                        "include_date_parameter": "y",
                        "output_format": fmt,
                        "author_name": "Test User",
                        "author_email": "test@test.com"
                    }
                )
                
                # Verify task was created with correct format
                assert os.path.exists(result)
                task_file = Path(result) / f"test{fmt}task.py"
                assert task_file.exists()
                
                content = task_file.read_text()
                assert f".{fmt}" in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
