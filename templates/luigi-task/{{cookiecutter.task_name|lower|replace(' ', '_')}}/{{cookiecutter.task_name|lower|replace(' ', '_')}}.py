"""
{{ cookiecutter.task_description }}

Author: {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
Created: {% raw %}{{ "now"|date("%Y-%m-%d") }}{% endraw %}
"""
{% if cookiecutter.include_date_parameter == "y" %}from datetime import datetime{% endif %}

import luigi
from luigi import LocalTarget
from pipelines_planejamento.settings import {% if cookiecutter.task_type == "extract" %}RAW_DATA_PATH{% elif cookiecutter.task_type == "transform" %}PROCESSED_DATA_PATH{% elif cookiecutter.task_type == "load" %}OUTPUT_DATA_PATH{% else %}PROCESSED_DATA_PATH{% endif %}

{% if cookiecutter.output_format == "csv" or cookiecutter.output_format == "excel" or cookiecutter.output_format == "parquet" %}import pandas as pd
{% endif %}

class {{ cookiecutter.task_name }}(luigi.Task):
    """
    {{ cookiecutter.task_description }}
    
    {% if cookiecutter.task_type == "extract" %}Extracts data from source and saves raw data.
    {% elif cookiecutter.task_type == "transform" %}Transforms raw data into processed format.
    {% elif cookiecutter.task_type == "load" %}Loads processed data to final destination.
    {% else %}Processes data according to business logic.
    {% endif %}
    """
    {% if cookiecutter.include_date_parameter == "y" %}
    date = luigi.DateParameter(default=datetime.now().date())
    {% endif %}
    
    {% if cookiecutter.include_requires == "y" %}def requires(self):
        """
        Define task dependencies here.
        Example: return [DependencyTask(date=self.date)]
        """
        # TODO: Add your task dependencies
        return []
    {% endif %}
    
    def output(self):
        """Define the output target for this task."""
        {% if cookiecutter.include_date_parameter == "y" %}filename = "{{ cookiecutter.task_name|lower|replace(' ', '_') }}_{}.{{ cookiecutter.output_format }}".format(self.date){% else %}filename = "{{ cookiecutter.task_name|lower|replace(' ', '_') }}.{{ cookiecutter.output_format }}"{% endif %}
        
        return [LocalTarget({% if cookiecutter.task_type == "extract" %}RAW_DATA_PATH{% elif cookiecutter.task_type == "transform" %}PROCESSED_DATA_PATH{% elif cookiecutter.task_type == "load" %}OUTPUT_DATA_PATH{% else %}PROCESSED_DATA_PATH{% endif %} / filename)]
    
    def run(self):
        """Main task execution logic."""
        {% if cookiecutter.task_type == "extract" %}# TODO: Implement data extraction logic
        # Example: Extract data from API, database, or file
        data = self._extract_data()
        
        # Save raw data
        {% if cookiecutter.output_format == "csv" %}df = pd.DataFrame(data)
        df.to_csv(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "json" %}import json
        with self.output()[0].open('w') as f:
            json.dump(data, f, indent=2)
        {% elif cookiecutter.output_format == "excel" %}df = pd.DataFrame(data)
        df.to_excel(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "parquet" %}df = pd.DataFrame(data)
        df.to_parquet(self.output()[0].path, index=False)
        {% endif %}{% elif cookiecutter.task_type == "transform" %}# TODO: Implement data transformation logic
        {% if cookiecutter.include_requires == "y" %}# Load data from dependencies
        # input_data = self._load_input_data()
        {% endif %}
        # Transform data
        # transformed_data = self._transform_data(input_data)
        
        # Save transformed data
        {% if cookiecutter.output_format == "csv" %}# df = pd.DataFrame(transformed_data)
        # df.to_csv(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "json" %}# import json
        # with self.output()[0].open('w') as f:
        #     json.dump(transformed_data, f, indent=2)
        {% elif cookiecutter.output_format == "excel" %}# df = pd.DataFrame(transformed_data)
        # df.to_excel(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "parquet" %}# df = pd.DataFrame(transformed_data)
        # df.to_parquet(self.output()[0].path, index=False)
        {% endif %}pass
        {% elif cookiecutter.task_type == "load" %}# TODO: Implement data loading logic
        {% if cookiecutter.include_requires == "y" %}# Load processed data from dependencies
        # processed_data = self._load_processed_data()
        {% endif %}
        # Load to final destination (database, API, file storage)
        # self._load_to_destination(processed_data)
        
        # Save load confirmation or report
        {% if cookiecutter.output_format == "csv" %}# df = pd.DataFrame(load_results)
        # df.to_csv(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "json" %}# import json
        # with self.output()[0].open('w') as f:
        #     json.dump(load_results, f, indent=2)
        {% endif %}pass
        {% else %}# TODO: Implement your task logic here
        {% if cookiecutter.output_format == "csv" %}# Example: Create a sample DataFrame
        # df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        # df.to_csv(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "json" %}# import json
        # data = {'key': 'value'}
        # with self.output()[0].open('w') as f:
        #     json.dump(data, f, indent=2)
        {% elif cookiecutter.output_format == "excel" %}# df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        # df.to_excel(self.output()[0].path, index=False)
        {% elif cookiecutter.output_format == "parquet" %}# df = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
        # df.to_parquet(self.output()[0].path, index=False)
        {% endif %}pass
        {% endif %}
    {% if cookiecutter.task_type == "extract" %}
    def _extract_data(self):
        """Extract data from source."""
        # TODO: Implement extraction logic
        # Example: API call, database query, file reading
        return []
    {% elif cookiecutter.task_type == "transform" %}
    {% if cookiecutter.include_requires == "y" %}def _load_input_data(self):
        """Load data from input dependencies."""
        # TODO: Implement input data loading
        return []
    {% endif %}
    def _transform_data(self, data):
        """Transform input data."""
        # TODO: Implement transformation logic
        return data
    {% elif cookiecutter.task_type == "load" %}
    {% if cookiecutter.include_requires == "y" %}def _load_processed_data(self):
        """Load processed data from dependencies."""
        # TODO: Implement processed data loading
        return []
    {% endif %}
    def _load_to_destination(self, data):
        """Load data to final destination."""
        # TODO: Implement loading logic (database, API, storage)
        pass
    {% endif %}


if __name__ == "__main__":
    # Run the task for testing
    task = {{ cookiecutter.task_name }}()
    luigi.build([task], local_scheduler=True)
