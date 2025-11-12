#!/usr/bin/env python
"""
CLI tool to generate Luigi pipeline components using Cookiecutter templates.

Usage:
    python generate.py task        # Generate a new Luigi task
    python generate.py spider      # Generate a new Scrapy spider
    python generate.py pipeline    # Generate a new pipeline project
"""
import os
import sys
from pathlib import Path
import argparse
from cookiecutter.main import cookiecutter


# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"


def generate_task(output_dir=None):
    """Generate a new Luigi task from template."""
    template_path = str(TEMPLATES_DIR / "luigi-task")

    if output_dir is None:
        output_dir = str(PROJECT_ROOT / "src" / "{{ "{{ cookiecutter.project_slug }}" }}" / "tasks")

    print("\n🚀 Generating Luigi Task...")
    print(f"Template: {template_path}")
    print(f"Output: {output_dir}\n")

    try:
        result = cookiecutter(
            template_path,
            output_dir=output_dir,
        )
        print(f"\n✅ Task generated successfully at: {result}")
        print("\n📝 Next steps:")
        print("1. Review and customize the generated task")
        print("2. Import the task in your tasks/__init__.py")
        print("3. Test the task with: luigi --module {{ cookiecutter.project_slug }}.tasks YourTask --local-scheduler")
        return result
    except Exception as e:
        print(f"\n❌ Error generating task: {e}")
        sys.exit(1)


def generate_spider(output_dir=None):
    """Generate a new Scrapy spider from template."""
    template_path = str(TEMPLATES_DIR / "scrapy-spider")

    if output_dir is None:
        output_dir = str(PROJECT_ROOT / "src" / "{{ "{{ cookiecutter.project_slug }}" }}" / "spiders")

    print("\n🚀 Generating Scrapy Spider...")
    print(f"Template: {template_path}")
    print(f"Output: {output_dir}\n")

    try:
        result = cookiecutter(
            template_path,
            output_dir=output_dir,
        )
        print(f"\n✅ Spider generated successfully at: {result}")
        print("\n📝 Next steps:")
        print("1. Review and customize the generated spider")
        print("2. Update selectors and parsing logic")
        print("3. Test the spider with: scrapy crawl spider_name")
        return result
    except Exception as e:
        print(f"\n❌ Error generating spider: {e}")
        sys.exit(1)


def generate_pipeline(output_dir=None):
    """Generate a new pipeline project from template."""
    template_path = str(TEMPLATES_DIR / "new-pipeline")

    if output_dir is None:
        output_dir = os.getcwd()

    print("\n🚀 Generating New Pipeline Project...")
    print(f"Template: {template_path}")
    print(f"Output: {output_dir}\n")

    try:
        result = cookiecutter(
            template_path,
            output_dir=output_dir,
        )
        print(f"\n✅ Pipeline project generated successfully at: {result}")
        print("\n📝 Next steps:")
        print("1. cd into the project directory")
        print("2. Create a virtual environment: uv venv")
        print("3. Install dependencies: uv sync")
        print("4. Configure .env file")
        print("5. Start building your pipeline!")
        return result
    except Exception as e:
        print(f"\n❌ Error generating pipeline: {e}")
        sys.exit(1)


def list_templates():
    """List available templates."""
    print("\n📋 Available Templates:\n")

    templates = {
        "task": "Luigi Task - Generate a new Luigi task for ETL operations",
        "spider": "Scrapy Spider - Generate a new Scrapy spider for web scraping",
        "pipeline": "Pipeline Project - Generate a complete new pipeline project",
    }

    for name, description in templates.items():
        print(f"  • {name:12} - {description}")

    print("\nUsage: python generate.py <template_name>")
    print("Example: python generate.py task\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Luigi pipeline components from Cookiecutter templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py task              # Generate a Luigi task
  python generate.py spider            # Generate a Scrapy spider
  python generate.py pipeline          # Generate a new pipeline project
  python generate.py --list            # List available templates
        """,
    )

    parser.add_argument("template", nargs="?", choices=["task", "spider", "pipeline"], help="Template to generate")

    parser.add_argument(
        "-o", "--output-dir", help="Output directory (default: appropriate directory for template type)"
    )

    parser.add_argument("-l", "--list", action="store_true", help="List available templates")

    args = parser.parse_args()

    if args.list or args.template is None:
        list_templates()
        sys.exit(0)

    # Generate based on template type
    generators = {
        "task": generate_task,
        "spider": generate_spider,
        "pipeline": generate_pipeline,
    }

    generator = generators[args.template]
    generator(args.output_dir)


if __name__ == "__main__":
    main()
