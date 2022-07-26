import os
import json
import time
from scrapy import Request, Spider


class ParseOpenCriticDirectly(Spider):
    """
    parse all selected values from the videogames
    """
    name = 'opencritic_games'

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

    def parse(self, response) -> dict:
        img = response.css('div.header-image-container')
        img = img.css('picture')
        img = img.css('img').attrib.get('src')
        img = img if img else ''

        name = response.css('h1.mb-0::text').get().strip()
        companies = response.css('div.companies')
        companies = [f.strip() for f in companies.css('span::text').getall()]
        companies = [f[:-1].strip() if f[-1] == ',' else f for f in companies]
        platforms = response.css('div.platforms')
        platforms = platforms.css('span')
        platforms = platforms.css('strong::text').getall()
        
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

        released = response.css('div.platforms::text').get().replace('-', '').strip()
        date, year = released.split(', ')
        link = response.css('div.text-right.my-1')
        link = link.css('a')
        critics_number = link.css('::text')
        critics_number = critics_number.get().strip() if critics_number else '0'
        critics_number = int("".join(filter(str.isdigit, critics_number)))
        critics_link = f"https://opencritic.com{link.attrib.get('href')}" \
            if link.attrib.get('href') else ''
        yield {
            'name': name,
            'companies': companies,
            'platforms': platforms,
            'score': score,
            'recommend': recommend,
            'released': released,
            'released_date': date,
            'released_year': int(year),
            'critics_number': critics_number,
            'critics_link': critics_link,
            'image': img,
        }
