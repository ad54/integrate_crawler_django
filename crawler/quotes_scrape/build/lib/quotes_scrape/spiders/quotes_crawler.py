# -*- coding: utf-8 -*-
import scrapy
from quotes_scrape.items import QuotesScrapeItem
import os
from datetime import datetime


class QuotesCrawlerSpider(scrapy.Spider):
    name = 'quotes_crawler'
    allowed_domains = []
    start_urls = []

    def __init__(self,keyword='', name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.keyword= keyword
        url = f'http://quotes.toscrape.com/tag/{keyword}/'
        self.start_urls.append(url)
        print(self.start_urls)
        try:
            self.job_id = os.environ['SCRAPY_JOB']
        except Exception as e:
            self.job_id = str(datetime.now())
            print('during job id : ',e)

    def parse(self, response):
        for div in response.xpath('//div[@class="quote"]'):
            item = QuotesScrapeItem()
            item['job_id'] = self.job_id
            item['quote_text'] = (div.xpath('.//span[@class="text"]/text()').get(default='')).strip('"').strip("'")
            item['quote_author'] = div.xpath('.//small[@class="author"]/text()').get(default='')
            item['quote_tags'] = div.xpath('.//meta[@class="keywords"]/@content').get(default='')
            item['input'] = self.keyword[:249]
            yield item

from scrapy.cmdline import execute
# execute('scrapy crawl quotes_crawler -a keyword=life'.split())
