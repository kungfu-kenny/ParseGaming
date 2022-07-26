import time
from scrapy import Spider
from parsegaming.items import GameListingOpencriticItem


class ParseOpenCritic(Spider):
    name = 'opencritic_listing'
    start_urls = [
        'https://opencritic.com/browse/all'
    ]

    @staticmethod
    def parse_name_link(response:object) -> set:
        """
        Static method which is dedicated to parse name and link
        Input:  responce = scrapy object
        Output: set with strings of name and link
        """
        ch = response.css('div.game-name.col')
        name = ch.css('a::text').get()
        link = f"https://opencritic.com{ch.css('a').attrib.get('href')}"
        id = int(link.split('/')[4]) if len(link.split('/')) > 5 else -1
        return name, link, id
            
    @staticmethod
    def parse_released(response:object) -> str:
        """
        Static method which is dedicated to parse released date
        Input:  responce = our scrapy object
        Output: string of the date
        """
        datetime = response.css('div.first-release-date.col-auto.show-year > span::text').get().strip()
        date, year = datetime.split(',')
        date, year = date.strip(), int(year.strip())
        return datetime, date, year

    @staticmethod
    def parse_type(response:object) -> str:
        """
        Static method which is dedicated to parse name and link
        Input:  responce = scrapy object
        Output: string of the new
        """
        img = response.css('div.tier.col-auto > img')
        if img:
            return img.attrib.get('alt')
        return ''

    @staticmethod
    def parse_link_next(response:object) -> set:
        """
        Method which is dedicated to produce the next link for search
        Input:  responce = scrapy object
        """
        class_new = response.css('div.col-md-12.text-center.text-md-right')
        rels = [f.attrib.get('rel') for f in class_new.css('a')]
        links = [
            f"https://opencritic.com{f.attrib.get('href')}" for f in class_new.css('a')
        ]
        if not 'next' in rels: 
            return False, ''
        ind = rels.index('next')
        return True, links[ind]

    def parse(self, response:object) -> dict:
        """
        Method which is dedicated to parse all of the all-time best titles
        Input:  response = responce of the selected link
        Output: dictionary of the values
        """
        item = GameListingOpencriticItem()
        for game in response.css('div.row.no-gutters.py-2.game-row.align-items-center'):
            item['status_press'] = self.parse_type(game)
            item['release'], item['date'], item['year'] = self.parse_released(game)
            item['name'], item['link'], item['id'] = self.parse_name_link(game)
            item['rank'] = int(
                game.css('div.rank::text').get().replace('.', '').strip()
            )
            item['score'] = game.css('div.score::text').get().strip()
            item['platforms'] = game.css('div.platforms.col-auto::text').get().strip(),
            yield item
        next_bool, next_link = self.parse_link_next(response)
        if next_bool:
            time.sleep(0.1)
            yield response.follow(next_link, callback=self.parse)