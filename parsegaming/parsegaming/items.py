# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class GameListingOpencriticItem(scrapy.Item):
    id = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    rank = scrapy.Field()
    companies = scrapy.Field()
    platforms = scrapy.Field()
    image = scrapy.Field()
    release = scrapy.Field()
    year = scrapy.Field()
    date = scrapy.Field()
    link_reviews = scrapy.Field()
    reviews_number = scrapy.Field()
    status_press = scrapy.Field()
    
class GameDirectlyOpencriticItem(scrapy.Item):
    id = scrapy.Field()
    rank = scrapy.Field()
    score = scrapy.Field()
    name = scrapy.Field()
    platform = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    release = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    companies = scrapy.Field()
    status_press = scrapy.Field()
    link_reviews = scrapy.Field()
    reviews_number = scrapy.Field()

class GameListingMetacriticItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    platform = scrapy.Field()
    release = scrapy.Field()
    date = scrapy.Field()
    year = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    score_link = scrapy.Field()
    image = scrapy.Field()

class GameDirectlyMetacriticItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    response = scrapy.Field()
    company = scrapy.Field()
    release = scrapy.Field()
    rating = scrapy.Field()
    platform = scrapy.Field()
    link_platform = scrapy.Field()
    reviews = scrapy.Field()
    reviews_user = scrapy.Field()
    link_reviews = scrapy.Field()
    link_users = scrapy.Field()
    genres = scrapy.Field()
    score = scrapy.Field()
    score_user = scrapy.Field()
    status_press = scrapy.Field()
    status_user = scrapy.Field()
    developers = scrapy.Field()
    link = scrapy.Field()
    link_company = scrapy.Field()
    link_developers = scrapy.Field()
    description = scrapy.Field()