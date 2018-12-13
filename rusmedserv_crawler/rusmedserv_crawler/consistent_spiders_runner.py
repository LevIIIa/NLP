# -*- coding: utf-8 -*-
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from rusmedserv_crawler.spiders.sections import SectionsSpider
from rusmedserv_crawler.spiders.themes import ThemesSpider
from rusmedserv_crawler.spiders.discussions import DiscussionsSpider

configure_logging()
runner = CrawlerRunner(get_project_settings())

# последовательный запуск пауков
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(SectionsSpider)
    yield runner.crawl(ThemesSpider)
    yield runner.crawl(DiscussionsSpider)
    reactor.stop()

crawl()
reactor.run()
