"""
This Scrapy example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#downloader-middleware;
- https://doc.scrapy.org/en/latest/topics/item-pipeline.html;
- https://doc.scrapy.org/en/latest/topics/media-pipeline.html;
- https://doc.scrapy.org/en/latest/topics/media-pipeline.html#using-the-images-pipeline.

Comparision of CSS selectors and Xpaths:
https://devhints.io/xpath
"""
from typing import Any
import scrapy
from scrapy.http.response import Response

BASE_URL = "en.wikipedia.org"
NOBEL_WINNERS_BY_COUNTRY_URL = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"


class NobelWinnerItem(scrapy.Item):
    """
    Contains the fields for the scraped data.
    """
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()


class NobelWinnersSpider(scrapy.Spider):
    """
    Scrapes the country and link text of the Nobel-winners.
    """
    name = 'Nobel_winners'
    allowed_domains = [BASE_URL]
    start_urls = [NOBEL_WINNERS_BY_COUNTRY_URL]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        country_item_list = response.xpath('//ol[1]/../h3')
        for country_item in country_item_list:
            winner_item_list = country_item.xpath('following-sibling::ol[1]/li')
            for winner_item in winner_item_list:
                country = country_item.xpath('span[@class="mw-headline"]/text()').extract()
                text = winner_item.xpath('descendant-or-self::text()').extract()
                yield NobelWinnerItem(
                    country=country[0],
                    name=text[0],
                    link_text=' '.join(text)
                )


