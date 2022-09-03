from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner


@defer.inlineCallbacks
def run_scraping(runner: CrawlerRunner):
    yield runner.crawl('opencritic_listing')

    yield runner.crawl('opencritic_source_data')
    reactor.stop()

def main():

    try:
        run_scraping(
            runner=CrawlerRunner(),
        )

        reactor.run()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
