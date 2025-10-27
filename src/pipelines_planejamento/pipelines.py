"""
Pipelines do Scrapy para processar items extraídos.
Cada pipeline pode validar, limpar, transformar ou armazenar dados.
"""

import csv
from datetime import datetime

from itemadapter import ItemAdapter

from pipelines_planejamento.settings import OUTPUT_DATA_PATH


class DataValidationPipeline:
    """
    Pipeline para validar dados básicos dos items.
    Garante que campos obrigatórios estão presentes.
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Adicionar timestamp de extração se não existir
        if not adapter.get("data_extracao"):
            adapter["data_extracao"] = datetime.now().isoformat()

        # Adicionar fonte se não existir
        if not adapter.get("fonte"):
            adapter["fonte"] = spider.name

        return item


class ValueNormalizationPipeline:
    """
    Pipeline para normalizar valores monetários do formato brasileiro.
    Converte strings como "R$ 1.234,56" para float 1234.56
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Normalizar campo 'valor' se existir
        if adapter.get("valor"):
            valor_str = str(adapter["valor"])
            try:
                # Remover R$, pontos de milhares e trocar vírgula por ponto
                valor_limpo = (
                    valor_str.replace("R$", "")
                    .replace("r$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                adapter["valor"] = float(valor_limpo)
            except (ValueError, AttributeError) as e:
                spider.logger.warning(
                    f"Não foi possível converter valor '{valor_str}': {e}"
                )
                adapter["valor"] = None

        return item


class DuplicatesPipeline:
    """
    Pipeline para detectar e filtrar items duplicados.
    """

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Use um campo único como identificador (ajuste conforme necessário)
        item_id = adapter.get("contrato") or adapter.get("identificador")

        if item_id:
            if item_id in self.ids_seen:
                spider.logger.info(f"Item duplicado encontrado: {item_id}")
                raise DropItem(f"Item duplicado: {item_id}")
            else:
                self.ids_seen.add(item_id)

        return item


class JsonExportPipeline:
    """
    Pipeline para exportar dados para JSON.
    Alternativa: usar o built-in FEEDS do Scrapy em settings.py
    """

    def open_spider(self, spider):
        # Placeholder: você pode inicializar arquivos/conexões aqui
        pass

    def close_spider(self, spider):
        # Placeholder: fechar conexões, finalizar arquivos
        pass

    def process_item(self, item, spider):
        # Placeholder: implementar lógica de export customizada se necessário
        # Por padrão, use FEEDS em settings.py
        return item


class CsvExportPipeline:
    """
    Pipeline para exportar dados para CSV no OUTPUT_DATA_PATH/outputs/.
    """

    def __init__(self):
        self.items = []
        self.fieldnames = set()

    def open_spider(self, spider):
        spider.logger.info("Iniciando coleta de dados para CSV")

    def close_spider(self, spider):
        if not self.items:
            spider.logger.info("Nenhum item coletado para CSV")
            return

        # Criar diretório se não existir
        output_dir = OUTPUT_DATA_PATH / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Nome do arquivo baseado no nome da spider e data atual
        filename = f"{spider.name}_{datetime.now().strftime('%Y-%m-%d')}.csv"
        filepath = output_dir / filename

        # Escrever CSV
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            if self.fieldnames:
                writer = csv.DictWriter(csvfile, fieldnames=sorted(self.fieldnames))
                writer.writeheader()

                for item_dict in self.items:
                    # Garantir que todas as colunas estejam presentes
                    for field in self.fieldnames:
                        if field not in item_dict:
                            item_dict[field] = ""
                    writer.writerow(item_dict)

        spider.logger.info(
            f"Export CSV finalizado: {len(self.items)} linhas, {len(self.fieldnames)} colunas em {filepath}"
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_dict = dict(adapter)

        # Coletar todos os fieldnames possíveis
        self.fieldnames.update(item_dict.keys())

        # Armazenar o item
        self.items.append(item_dict)

        return item
