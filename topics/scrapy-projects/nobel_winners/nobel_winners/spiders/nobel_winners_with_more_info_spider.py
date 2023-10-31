import re

from typing import Any, Dict
import scrapy
from scrapy import Selector
from scrapy.http.response import Response

BASE_URL = "en.wikipedia.org"
NOBEL_WINNERS_BY_COUNTRY_URL = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
YEAR_PATTERN = re.compile(r'\d{4}')
CATEGORY_PATTERN = re.compile(r'Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economics')


class NobelWinnerItem(scrapy.Item):
    """
    Contains the fields for the scraped data.
    """
    country = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    born_in = scrapy.Field()
    gender = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()


class NobelWinnersSpider(scrapy.Spider):
    """
    Scrapes the country and link text of the Nobel-winners.
    """
    name = 'Nobel_winners_with_more_info'
    allowed_domains = [BASE_URL]
    start_urls = [NOBEL_WINNERS_BY_COUNTRY_URL]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        country_item_list = response.xpath('//ol[1]/../h3')
        for country_item in country_item_list:
            winner_item_list = country_item.xpath('following-sibling::ol[1]/li')
            for winner_item in winner_item_list:
                country = country_item.xpath('span[@class="mw-headline"]/text()').extract()
                winner_data = self._process_winner_li(winner_item, country[0])
                yield NobelWinnerItem(
                    country=winner_data['country'],
                    name=winner_data['name'],
                    year=winner_data['year'],
                    category=winner_data['category'],
                    born_in=winner_data['born_in'],
                    link=winner_data['link'],
                    text=winner_data['text'],
                )

    @staticmethod
    def _process_winner_li(winner_item: Selector, country=None) -> Dict[str, str | int]:
        """
        Process a winner's <li> tag, adding country of birth or nationality, as applicable.
        """
        text = ' '.join(winner_item.xpath('descendant-or-self::text()').extract())
        year = YEAR_PATTERN.findall(text)
        category = CATEGORY_PATTERN.findall(text)
        asteriks = text.find("*")
        data = {
            # Get the href link-address from the <a> tag
            'link': BASE_URL + winner_item.xpath('a/@href').extract()[0],
            # Get comma-delineated name and strip trailing whitespace
            'name': text.split(',')[0].strip(),
            'year': int(year[0]) if year else None,
            'category': category if category else None,
            'country': country if asteriks == -1 else None,
            'born_in': country if asteriks != -1 else None,
            'text': text
        }
        return data

# //*[@id="Q190697$2E6DAE31-5A4E-4A6D-8EF3-5933B7BD2807"]/div[2]/div[1]/div/div[2]/div[2]/div[1]