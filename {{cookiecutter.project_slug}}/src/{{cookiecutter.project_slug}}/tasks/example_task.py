import subprocess
from datetime import datetime

import luigi
from luigi import LocalTarget
from {{ cookiecutter.project_slug }}.settings import PROCESSED_DATA_PATH


class ExampleTask(luigi.Task):
    date = luigi.DateParameter(default=datetime.now().date())
    initial_date = luigi.DateParameter(default=datetime.now().replace(day=1))

    def output(self):
        filename = f"raw_data_test_{self.date}.csv"
        # Retornar como lista para manter consistência com outras tasks
        return [LocalTarget(PROCESSED_DATA_PATH / filename)]

    def run(self):
        out_path = str(self.output()[0].path)
        # Aqui você pode adicionar a lógica para processar os dados
        # Por exemplo, você pode usar o subprocess para chamar um comando externo
        cmd = [
            "python",
            "process_data.py",
            "--output",
            out_path,
        ]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    # Você pode rodar esse arquivo para testar a task
    task = ExampleTask()
    luigi.build([task], local_scheduler=True)
