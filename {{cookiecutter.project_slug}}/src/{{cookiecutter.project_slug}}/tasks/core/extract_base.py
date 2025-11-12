import logging
import sys
from abc import ABC, abstractmethod
from datetime import date as dt_date
from datetime import datetime
from pathlib import Path

import pandas as pd

import luigi

from {{ cookiecutter.project_slug }}.settings import OUTPUT_DATA_PATH

logger = logging.getLogger("luigi-interface")

# Aqui você pode definir tasks base quando houver tarefas que se repitam em muitas tasks
# No caso abaixo, defini uma base task que lida com a extração de dados de planilhas do Google
# Precisamos apenas sobrescrever o método de transformação para cada task específica

class BaseExtractTask(luigi.Task, ABC):
    """
    Base class for extracting data from Google Sheets.
    Provides common extract logic and abstract transform method.
    """

    date = luigi.DateParameter(default=datetime.now().date())

    def requires(self):
        """Define task dependencies - none for extract tasks"""
        return []

    def output(self):
        """Define the output target"""
        filename = f"final_output_{self.output_prefix}_{self.date}.csv"
        return [luigi.LocalTarget(OUTPUT_DATA_PATH / filename)]

    def run(self):
        """Execute the extract logic"""
        logger.info(
            f"Starting extract for {self.output_prefix} on {self.worksheet_name} for date {self.date}"
        )

        # Extract data
        data = self._extract_data()

        # Transform data (specific to each task)
        df_transformed = self._transform_data(data)

        # Write output
        self._write_output(df_transformed)

        # Generate summary
        self._generate_summary_report(df_transformed)

    def _extract_data(self):
        """Common extract logic using SheetsClient"""
        logger.info("Reading data from Google Sheets")
       

    @abstractmethod
    def _transform_data(self, data) -> pd.DataFrame:
        """Abstract method for specific transformation logic"""
        pass

    def _write_output(self, df: pd.DataFrame):
        """Common write logic"""
        out_path = self.output()[0].path
        df.to_csv(out_path, index=False, encoding="utf-8")
        logger.info(f"Wrote output to {out_path} ({len(df)} rows)")

    def _generate_summary_report(self, df: pd.DataFrame) -> None:
        """Generate a summary report"""
        report_file = OUTPUT_DATA_PATH / f"summary_{self.output_prefix}_{self.date}.txt"
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                f.write("Data Pipeline Summary Report\n")
                f.write(("=" * 50) + "\n\n")
                f.write(f"Date: {self.date}\n")
                f.write(f"Sheet: {self.worksheet_name}\n")
                f.write(f"Output: {self.output_prefix}\n")
                f.write(f"Total Records: {len(df)}\n\n")
                f.write(f"Generated at: {datetime.now()}\n")
            logger.info(f"Summary report generated: {report_file}")
        except Exception as e:
            logger.error(f"Failed to write summary report: {e}")


if __name__ == "__main__":
    # Example usage - replace with actual task
    pass
