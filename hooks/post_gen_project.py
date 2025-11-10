#!/usr/bin/env python
"""
Post-generation hook for Cookiecutter template.

This script runs after the project is generated to:
- Remove optional components based on user choices
- Clean up unused files
- Display next steps
"""
import os
import shutil
from pathlib import Path


def remove_dir(filepath):
    """Remove a directory and all its contents."""
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)


def remove_file(filepath):
    """Remove a file."""
    if os.path.isfile(filepath):
        os.remove(filepath)


def main():
    """Execute post-generation cleanup."""
    project_slug = "{{ cookiecutter.project_slug }}"
    include_scrapy = "{{ cookiecutter.include_scrapy }}"
    include_fastapi = "{{ cookiecutter.include_fastapi }}"
    include_scheduler = "{{ cookiecutter.include_scheduler }}"
    
    src_dir = Path("src") / project_slug
    
    # Remove Scrapy-related components if not included
    if include_scrapy != "y":
        remove_dir(src_dir / "spiders")
        remove_dir(src_dir / "scrapers")
        remove_file("scrapy.cfg")
        remove_file(src_dir / "items.py")
        remove_file(src_dir / "middlewares.py")
        remove_file(src_dir / "pipelines.py")
        print("✓ Scrapy components removed")
    
    # Remove FastAPI components if not included
    if include_fastapi != "y":
        remove_dir(src_dir / "api")
        print("✓ FastAPI components removed")
    
    # Remove Scheduler components if not included
    if include_scheduler != "y":
        remove_dir(src_dir / "scheduler")
        print("✓ Scheduler components removed")
    
    print("\n" + "="*60)
    print("🎉 Project '{{ cookiecutter.project_name }}' created successfully!")
    print("="*60)
    print("\n📝 Next steps:")
    print("\n1. Navigate to your project:")
    print(f"   cd {{ cookiecutter.project_slug }}")
    print("\n2. Create and activate a virtual environment:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # Linux/Mac")
    print("   # or: venv\\Scripts\\activate  # Windows")
    print("\n3. Install dependencies:")
    print("   pip install -e .")
    print("\n4. Configure your environment:")
    print("   cp .env.example .env")
    print("   cp luigi.cfg.example luigi.cfg")
    if include_scrapy == "y":
        print("   cp scrapy.cfg.example scrapy.cfg")
    print("\n5. Start building your pipeline!")
    print(f"   # Edit src/{project_slug}/tasks/example_task.py")
    print("\n📚 Documentation: See README.md for detailed instructions")
    print("\n")


if __name__ == "__main__":
    main()
