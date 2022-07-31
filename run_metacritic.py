from scrapy import Spider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from parsegaming.parsegaming.spiders.parse_metacritic_directly import ParseMetaCriticDirectly


@defer.inlineCallbacks
def run_scraping(runner: CrawlerRunner, spider: str):
    yield runner.crawl(spider)
    reactor.stop()

def main():

    try:
        run_scraping(
            runner=CrawlerRunner(),
            spider=ParseMetaCriticDirectly
        )
        reactor.run()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
