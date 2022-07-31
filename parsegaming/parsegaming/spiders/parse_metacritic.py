import time
from scrapy import Spider
from items import GameListingMetacriticItem


class ParseMetaCritic(Spider):
    name = 'metacritic'
    start_urls = [
        'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered'
    ]

    @staticmethod
    def parse_reviews(response) -> set:
        """
        Static method which is dedicated to parse reviews from the journalists
        Input:  response = response value
        Output: set with the link of the image and its scope
        """
        link_class = response.css('a.metascore_anchor')
        link = f"https://www.metacritic.com{link_class.attrib.get('href')}"
        score = link_class.css('div.metascore_w::text').get().strip()
        if score:
            return link, int(score)
        return link, 0

    @staticmethod
    def parse_name(response:object) -> set:
        """
        Static method which is dedicated to develop the link to game and its name
        Input:  response = object of the selected values
        Output: we developed string with name and link to it
        """
        res = response.css('a.title')
        return res.css('h3::text').get().strip(), \
            f"https://www.metacritic.com{res.attrib.get('href')}"

    @staticmethod
    def parse_platform(response:object) -> set:
        """
        Static method which is dedicated to get the platform from it
        Input:  response = object of the selected values
        Output: set of value platform and its release date
        """
        k = response.css('div.clamp-details')
        platform, release = [f.strip() for f in k.css('span::text').getall()][1:]
        date, year = release.split(',')
        date, year = date.strip(), int(year.strip())
        return release, date, year, platform

    def parse(self, response) -> dict:
        """
        Method which is dedicated to develop the parsing 
        Input:  response = css value of the page
        Output: dictionary with selected values
        """
        item = GameListingMetacriticItem()
        for block in response.css('table.clamp-list'):
            images = block.css('td.clamp-image-wrap')
            summaries = block.css('td.clamp-summary-wrap')
            for image, summary in zip(images, summaries): 
                item['description'] = summary.css('div.summary::text').get().strip()
                item['image'] = image.css('img').attrib.get('src')
                item['id'] = summary.css('input').attrib.get('id')
                item['name'], \
                    item['link'] = self.parse_name(summary)
                item['score_link'], \
                    item['score'] = self.parse_reviews(summary)
                item['release'], \
                    item['date'], \
                    item['year'], \
                    item['platform'] = self.parse_platform(summary)
                yield item
                
        next_link = response.css('span.flipper.next > a.action').attrib.get('href')
        if next_link:
            next_link = f"https://www.metacritic.com{next_link}"
            # time.sleep(0.2)
            # time.sleep(5.0)
            yield response.follow(next_link, callback=self.parse)