"""
Define aqui os modelos de dados (Items) para as spiders.
Scrapy Items são objetos simples que definem a estrutura dos dados extraídos.
"""

from scrapy import Field, Item


class PropostaItem(Item):
    """
    Item genérico para dados extraídos pela proposta_spider.
    """

    campo1 = Field()
    campo2 = Field()
    campo3 = Field()
    campo4 = Field()
