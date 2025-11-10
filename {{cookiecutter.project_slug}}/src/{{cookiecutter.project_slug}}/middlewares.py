"""
Middlewares customizados do Scrapy.
Você pode implementar Spider Middlewares e Downloader Middlewares aqui.
"""

from scrapy import signals


class CustomSpiderMiddleware:
    """
    Spider middleware para processar responses e exceptions.
    """

    @classmethod
    def from_crawler(cls, crawler):
        # Inicializar middleware com crawler
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Chamado para cada response que passa pelo spider
        return None

    def process_spider_output(self, response, result, spider):
        # Chamado com os resultados retornados pelo spider
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Chamado quando spider ou process_spider_input levanta exceção
        pass

    def process_start_requests(self, start_requests, spider):
        # Chamado com as start requests do spider
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class CustomDownloaderMiddleware:
    """
    Downloader middleware para processar requests/responses.
    Útil para adicionar headers, rotação de proxies, retry logic, etc.
    """

    @classmethod
    def from_crawler(cls, crawler):
        # Inicializar middleware com crawler
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Chamado para cada request antes de ser processado
        # Pode retornar None, Response, ou Request
        
        # Exemplo: adicionar headers customizados
        # request.headers['Custom-Header'] = 'value'
        
        return None

    def process_response(self, request, response, spider):
        # Chamado com a response retornada pelo download
        # Deve retornar Response ou Request
        
        # Exemplo: retry em status codes específicos
        # if response.status == 503:
        #     return request
        
        return response

    def process_exception(self, request, exception, spider):
        # Chamado quando download handler ou process_request levanta exceção
        # Deve retornar None, Response ou Request
        pass

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class RotateUserAgentMiddleware:
    """
    Middleware para rotacionar User-Agent em cada request.
    """
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        ]
        self.current_index = 0
    
    def process_request(self, request, spider):
        # Rotacionar user agent
        request.headers['User-Agent'] = self.user_agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.user_agents)
        return None
