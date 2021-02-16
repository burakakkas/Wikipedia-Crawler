import scrapy
import time
import traceback
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from category_crawler.spiders.category_crawler import CategoryCrawler
from page_crawler.spiders.page_crawler import PageCrawler

#function for sequential work of crawlers
def start_sequentially(process: CrawlerProcess, crawlers: list):
    print('start crawler {}'.format(crawlers[0].__name__))
    deferred = process.crawl(crawlers[0])
    if len(crawlers) > 1:
        deferred.addCallback(
            lambda _: start_sequentially(process, crawlers[1:]))

if __name__ == "__main__":
    try:
        #log level settings of crawler
        settings = get_project_settings()
        settings['LOG_LEVEL'] = 'INFO'
        settings['LOG_FILE'] = 'crawler.log'

        #starting crawlers
        crawlers = [CategoryCrawler, PageCrawler]
        process = CrawlerProcess(settings)
        start_sequentially(process, crawlers)
        process.start()

    #Error Handling
    except Exception:
        traceback.print_exc()
