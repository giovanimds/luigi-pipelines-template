"""
{{ cookiecutter.spider_description }}

Author: {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>
Created: {% raw %}{{ "now"|date("%Y-%m-%d") }}{% endraw %}
"""
{% if cookiecutter.spider_type == "basic" %}import scrapy


class {{ cookiecutter.spider_name|capitalize }}Spider(scrapy.Spider):
    """{{ cookiecutter.spider_description }}"""
    
    name = "{{ cookiecutter.spider_name }}"
    allowed_domains = ["{{ cookiecutter.allowed_domains }}"]
    start_urls = ["{{ cookiecutter.start_urls }}"]
    
    {% if cookiecutter.include_login == "y" %}def start_requests(self):
        """Start requests with login if needed."""
        # TODO: Implement login logic
        return [scrapy.Request(
            url="{{ cookiecutter.start_urls }}",
            callback=self.parse
        )]
    {% endif %}
    
    def parse(self, response):
        """Parse the response and extract data."""
        # TODO: Implement your parsing logic
        {% for item in cookiecutter.output_items.split(',') %}
        {{ item.strip() }} = response.css('selector::text').get()  # TODO: Update selector
        {% endfor %}
        
        yield {
            {% for item in cookiecutter.output_items.split(',') %}
            '{{ item.strip() }}': {{ item.strip() }},
            {% endfor %}
        }
        
        # Follow pagination links if needed
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
{% elif cookiecutter.spider_type == "crawl" %}import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class {{ cookiecutter.spider_name|capitalize }}Spider(CrawlSpider):
    """{{ cookiecutter.spider_description }}"""
    
    name = "{{ cookiecutter.spider_name }}"
    allowed_domains = ["{{ cookiecutter.allowed_domains }}"]
    start_urls = ["{{ cookiecutter.start_urls }}"]
    
    rules = (
        # Follow links matching the pattern and parse with parse_item
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )
    
    {% if cookiecutter.include_login == "y" %}def start_requests(self):
        """Start requests with login if needed."""
        # TODO: Implement login logic
        return [scrapy.Request(
            url="{{ cookiecutter.start_urls }}",
            callback=self.parse
        )]
    {% endif %}
    
    def parse_item(self, response):
        """Parse the response and extract data."""
        # TODO: Implement your parsing logic
        {% for item in cookiecutter.output_items.split(',') %}
        {{ item.strip() }} = response.css('selector::text').get()  # TODO: Update selector
        {% endfor %}
        
        yield {
            {% for item in cookiecutter.output_items.split(',') %}
            '{{ item.strip() }}': {{ item.strip() }},
            {% endfor %}
        }
{% elif cookiecutter.spider_type == "sitemap" %}import scrapy
from scrapy.spiders import SitemapSpider


class {{ cookiecutter.spider_name|capitalize }}Spider(SitemapSpider):
    """{{ cookiecutter.spider_description }}"""
    
    name = "{{ cookiecutter.spider_name }}"
    allowed_domains = ["{{ cookiecutter.allowed_domains }}"]
    sitemap_urls = ["{{ cookiecutter.start_urls }}/sitemap.xml"]
    
    def parse(self, response):
        """Parse the response and extract data."""
        # TODO: Implement your parsing logic
        {% for item in cookiecutter.output_items.split(',') %}
        {{ item.strip() }} = response.css('selector::text').get()  # TODO: Update selector
        {% endfor %}
        
        yield {
            {% for item in cookiecutter.output_items.split(',') %}
            '{{ item.strip() }}': {{ item.strip() }},
            {% endfor %}
        }
{% elif cookiecutter.spider_type == "csv_feed" %}import scrapy
from scrapy.spiders import CSVFeedSpider


class {{ cookiecutter.spider_name|capitalize }}Spider(CSVFeedSpider):
    """{{ cookiecutter.spider_description }}"""
    
    name = "{{ cookiecutter.spider_name }}"
    allowed_domains = ["{{ cookiecutter.allowed_domains }}"]
    start_urls = ["{{ cookiecutter.start_urls }}"]
    delimiter = ','
    quotechar = '"'
    
    # Column names in the CSV file
    headers = [{% for item in cookiecutter.output_items.split(',') %}'{{ item.strip() }}'{% if not loop.last %}, {% endif %}{% endfor %}]
    
    def parse_row(self, response, row):
        """Parse each row from the CSV."""
        # TODO: Implement your parsing logic
        yield {
            {% for item in cookiecutter.output_items.split(',') %}
            '{{ item.strip() }}': row['{{ item.strip() }}'],
            {% endfor %}
        }
{% endif %}
