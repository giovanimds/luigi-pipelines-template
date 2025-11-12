import subprocess
from datetime import datetime

import luigi
from luigi import LocalTarget
from {{ cookiecutter.project_slug }}.settings import PROCESSED_DATA_PATH


class RunPropostaSpiderTask(luigi.Task):
    date = luigi.DateParameter(default=datetime.now().date())
    initial_date = luigi.DateParameter(default=datetime.now().replace(day=1))

    def output(self):
        filename = f"proposta_{self.date}.csv"
        # Retornar como lista para manter consistência com outras tasks
        return [LocalTarget(PROCESSED_DATA_PATH / filename)]

    def run(self):
        out_path = str(self.output()[0].path)
        # Passar o caminho de saída via argumento do spider para evitar conflitos com o CLI do Scrapy
        cmd = [
            "scrapy",
            "crawl",
            "propostas_spider",
            "-a",
            f"output_path={out_path}",
        ]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    # Você pode rodar esse arquivo para testar a task
    task = RunPropostaSpiderTask()
    luigi.build([task], local_scheduler=True)
