from scrapy import Spider


class PropostasSpider(Spider):
    name = "propostas_spider"
    start_urls = ["https://example.com/"]

    def parse(self, response):
        # Exemplo simples: extrai título da página
        yield {
            "url": response.url,
            "title": response.xpath('//title/text()').get(),
        }
