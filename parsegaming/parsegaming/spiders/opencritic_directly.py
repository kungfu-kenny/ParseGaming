import os
import json
import time
from scrapy import Request, Spider
from parsegaming.items import GameDirectlyOpencriticItem


class ParseOpenCriticDirectly(Spider):
    """
    parse all selected values from the videogames
    """
    name = 'opencritic_source_data'

    def __init__(self) -> None:
        self.file = \
            ''

    def start_requests(self) -> object:
        """
        Method to get the link values from the json
        Input:  previously parsed values
        Output: object of the selected request value
        """
        if not os.path.exists(self.file):
            return
        with open(self.file, 'r') as json_used:
            value_list = json.load(json_used)
        urls = [f.get('link', '') for f in value_list if f]
        # urls = urls[:25]
        for url in urls:
            time.sleep(0.3)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = GameDirectlyOpencriticItem()
        img = response.css('div.header-image-container > picture > img').attrib.get('src')
        companies = [f.strip() for f in response.css('div.companies > span::text').getall()]

        values = response.css('div.inner-orb::text').getall()
        if len(values) == 2:
            score, recommend = [
                int(f.replace('%', '')) for f in response.css('div.inner-orb::text').getall()
            ]
        elif len(values) == 1:
            value = response.css('div.inner-orb::text').getall()[0]
            if '%' in value:
                score, recommend = -1, int(value.replace('%', ''))
            else:
                score, recommend = int(value.replace('%', '')), -1
        else:
            score, recommend = -1, -1

        release = response.css('div.platforms::text').get().replace('-', '').strip()
        date, year = release.split(', ')
        link = response.css('div.text-right.my-1 > a')
        
        critics_number = response.css('div.text-right.my-1 > a::text')
        critics_number = critics_number.get().strip() if critics_number else '0'
        
        item['image'] = img if img else ''
        item['name'] = response.css('h1.mb-0::text').get().strip()
        item['companies'] = [f[:-1].strip() if f[-1] == ',' else f for f in companies]
        item['platforms'] = response.css('div.platforms > span > strong::text').getall()
        item['score'] = score
        item['rank'] = recommend
        item['release'] = release
        item['date'] = date
        item['year'] = year
        item['link'] = response.request.url
        item['link_reviews'] = f"https://opencritic.com{link.attrib.get('href')}" \
            if link.attrib.get('href') else ''
        item['reviews_number'] = int("".join(filter(str.isdigit, critics_number)))

        yield item