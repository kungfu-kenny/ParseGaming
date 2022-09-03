import os
import json
import time
from fake_useragent import UserAgent
from scrapy import Spider, Request
from parsegaming.items import GameDirectlyMetacriticItem


class ParseMetaCriticDirectly(Spider):
    """
    Class which is dedicated to parse in metacritic directly
    """
    name = 'metacritic_source_data'

    def __init__(self):
        self.file = \
            '/home/oshevchenko/FolderProjects/ParseGaming/parsegaming/metacritic_alltime_best.json'

    def start_requests(self) -> list:
        """
        Method which is dedicated to make the 
        Input:  None
        Output: we developed list of the selected 
        """
        if not os.path.exists(self.file):
            return
        with open(self.file, 'r') as json_used:
            value_list = json.load(json_used)
        urls = [f.get('link', '') for f in value_list if f]
        urls = urls[:2]
        for url in urls:
            # time.sleep(0.3)
            yield Request(
                url=url,
                headers={'User-Agent': str(UserAgent().random)},
                callback=self.parse
            )

    @staticmethod
    def get_platform(response:object) -> set:
        """
        Static method which is dedicated to get information of the platforms
        Input:  response =
        Output: set with values of the 
        """
        platform = response.css('span.platform::text').get()#.strip()
        platform = platform.strip() if platform else ''
        if platform:
            return platform, ''
        platform = response.css('span.platform')
        platform = platform.css('a')
        pl = platform.attrib.get('href')
        link = f"https://www.metacritic.com{pl}" if pl else ''
        return platform.css('::text').get().strip() if platform.css('::text').get() else '', link

    @staticmethod
    def get_reviews(response:object) -> set:
        """
        Static method which is dedicated to get the reviews values to them
        Input:  response 
        """
        reviews = response.css('span.count')
        reviews = reviews.css('a')
        rev = reviews.attrib.get('href')
        reviews_link = f"https://www.metacritic.com{rev}" if rev else ''
        reviews_number = reviews.css('span::text').get()#.strip()
        return reviews_number if reviews_number else 0, reviews_link

    @staticmethod
    def get_users(response:object) -> set:
        """
        Static method which is dedicated to get the users of selected values
        Input:  response
        """
        userscore = response.css('div.userscore_wrap.feature_userscore')
        userscore = userscore.css('div.summary')
        userscore = userscore.css('p')
        user_desc = userscore.css('span.desc::text').get()#.strip()
        user_desc = user_desc.strip() if user_desc else ''
        user_counts = userscore.css('span.count')
        user_count = user_counts.css('a::text').get()#.strip()
        user_count = user_count.strip() if user_count else ''
        li = user_counts.css('a').attrib.get('href')
        user_link = f"https://www.metacritic.com{li}" if li else ''
        user_count = 0 if not user_count or not 'Ratings' in user_count else user_count.split('Ratings')[0].strip()
        return user_desc, int(user_count), user_link

    @staticmethod
    def get_developers(response:object) -> set:
        """
        Static method which is dedicated to get the developers of the game
        Input:  response = 
        """
        developers = response.css('li.summary_detail.developer')
        developers = developers.css('span.data')
        developers = developers.css('a.button')
        li = developers.attrib.get('href')
        link = f"https://www.metacritic.com{li}" if li else ''
        name = developers.css('::text').get()#.strip()
        name = name.strip() if name else ''
        return name, link

    def parse(self, response:object):
        item = GameDirectlyMetacriticItem()
        
        title_href = response.css('a.hover_none').attrib.get('href')
        title = response.css('a.hover_none > h1::text').get()
        company = response.css('span.data')
        co = company.css('a').attrib.get('href')
        company = company.css('a::text').get()
        release = response.css('li.summary_detail.release_data > span.data::text').get()
        
        item['platform'], \
            item['platform_link'] = self.get_platform(response)
        item['reviews'], \
            item['link_reviews'] = self.get_reviews(response)
        item['status_user'], \
            item['reviews_user'], \
            item['link_users'] = self.get_users(response)
        item['developers'], \
            item['link_developers'] = self.get_developers(response)
        item['name'] = title.strip() if title else ''
        item['link'] = f"https://www.metacritic.com{title_href}" if title_href else ''
        item['response'] = response.request.url
        item['release'] = release.strip() if release else ''
        item['rating'] = response.css('li.summary_detail.product_rating > span.data::text')
        item['company'] = company.strip() if company else ''
        item['score'] = response.css('div.metascore_w')
        item['genre'] = response.css('li.summary_detail.product_genre > span.data::text')
        item['link_company'] = f"https://www.metacritic.com{co}" if co else ''
        item['score_user'] = int(float(response.css('div.metascore_w.user::text').get())*10) \
            if response.css('div.metascore_w.user::text').get() else 0
        item['status_press'] = response.css('span.desc::text').get().strip() \
                if response.css('span.desc::text') else ''
        item['description']= response.css('span.blurb.blurb_expanded::text').get().strip() \
                if response.css('span.blurb.blurb_expanded::text') else ''
        yield item