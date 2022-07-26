import os
import json
import time
from fake_useragent import UserAgent
from scrapy import Spider, Request


class ParseMetaCriticDirectly(Spider):
    """
    Class which is dedicated to parse in metacritic directly
    """
    name = 'metacritic_games'

    def __init__(self):
        self.file = \
            ''

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
        for url in urls:
            time.sleep(0.3)
            yield Request(
                url=url,
                headers={'User-Agent': str(UserAgent())},
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
        return user_desc, user_count, user_link

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
        """
        Method which is dedicated to get values from it
        """
        title = response.css('a.hover_none')
        title_href = title.attrib.get('href')
        href = f"https://www.metacritic.com{title_href}" if title_href else ''
        title = title.css('h1::text').get()
        title = title.strip() if title else ''
        company = response.css('span.data')
        co = company.css('a').attrib.get('href')
        company_href = f"https://www.metacritic.com{co}" if co else ''
        company = company.css('a::text').get()
        company = company.strip() if company else ''
        released = response.css('li.summary_detail.release_data')
        released = released.css('span.data::text').get()
        released = released.strip() if released else ''
        score = response.css('div.metascore_w')
        rating = response.css('li.summary_detail.product_rating')
        rating = rating.css('span.data::text')
        genre = response.css('li.summary_detail.product_genre')
        platform, platform_link = self.get_platform(response)
        reviews, reviews_link = self.get_reviews(response)
        user_status, user_count, user_link = self.get_users(response)
        developers_name, developers_link = self.get_developers(response)
        yield {
            'title': title,
            'response': response.request.url,
            'company': company,
            'released': released,
            'rating': rating.get().strip() if rating else '',
            'platform': platform,
            'platform_link': platform_link,
            'reviews': int(reviews),
            'reviews_user': int(user_count),
            'reviews_link': reviews_link,
            'users_link': user_link,
            'genres': genre.css('span.data::text').getall(),
            'score': int(score.css('span::text').get()) if score.css('span::text').get() else 0,
            'user_score': int(float(response.css('div.metascore_w.user::text').get())*10) \
                if response.css('div.metascore_w.user::text').get() else 0,
            'status_press': response.css('span.desc::text').get().strip() \
                if response.css('span.desc::text') else '',
            'status_user': user_status,
            'developers': developers_name,
            'href': href,
            'company_href': company_href,
            'developers_link': developers_link,
            'description': response.css('span.blurb.blurb_expanded::text').get().strip() \
                if response.css('span.blurb.blurb_expanded::text').get() else ''
        }