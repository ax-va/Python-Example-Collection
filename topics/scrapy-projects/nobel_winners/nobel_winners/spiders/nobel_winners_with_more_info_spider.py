import re

from typing import Any, Dict
import scrapy
from scrapy import Selector
from scrapy.http.response import Response

WIKIPEDIA_DOMAIN = "en.wikipedia.org"
BASE_URL = "https://" + WIKIPEDIA_DOMAIN
NOBEL_WINNERS_BY_COUNTRY_URL = BASE_URL + "/wiki/List_of_Nobel_laureates_by_country"
YEAR_PATTERN = re.compile(r'\d{4}')
CATEGORY_PATTERN = re.compile(r'Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economics')
WIKIDATA_PROPERTIES= [
    {'name': 'date_of_birth', 'code': 'P569'},
    {'name': 'date_of_death', 'code': 'P570'},
    {'name': 'place_of_birth', 'code': 'P19', 'link': True},
    {'name': 'place_of_death', 'code': 'P20', 'link': True},
    {'name': 'gender', 'code': 'P21', 'link': True}
]


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
    wikidata_code = scrapy.Field()


class NobelWinnersSpider(scrapy.Spider):
    """
    Scrapes the country and link text of the Nobel-winners.
    """
    name = 'Nobel_winners_with_more_info'
    allowed_domains = [WIKIPEDIA_DOMAIN]
    start_urls = [NOBEL_WINNERS_BY_COUNTRY_URL]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        country_item_list = response.xpath('//ol[1]/../h3')
        for country_item in country_item_list:
            winner_item_list = country_item.xpath('following-sibling::ol[1]/li')
            for winner_item in winner_item_list:
                country = country_item.xpath('span[@class="mw-headline"]/text()').extract()
                winner_data = self._process_winner_li(winner_item, country[0])
                request = scrapy.Request(  # Make a request to the winner’s biography page
                    winner_data['link'],
                    callback=self.parse_personal_page,  # Set the callback function to handle the response
                    dont_filter=True
                )
                request.meta['item'] = NobelWinnerItem(**winner_data)
                yield request

    def parse_personal_page(self, response: Response):
        """
        Handles the callback from the biography-link request.
        """
        item = response.meta['item']
        href = response.xpath("//li[@id='t-wikibase']/a/@href").extract()
        if href:
            item['wikidata_code'] = href[0].split('/')[-1]
            request = scrapy.Request(
                href[0],
                callback=self.parse_wikidata,
                dont_filter=True
            )
            request.meta['item'] = item
            yield request

    def parse_wikidata(self, response: Response):
        """
        Parses wikidata to get additional data.
        """
        item = response.meta['item']
        for prop in WIKIDATA_PROPERTIES:
            link_html = '/a' if prop.get('link') else ''
            # Select the div with a property-code id
            code = prop["code"]
            code_block = response.xpath(f"//*[@id='{code}']")
            if code_block:
                # Use the css selector, which has superior class selection
                values = code_block.css('.wikibase-snakview-value')
                value = values[0]
                prop_sel = value.xpath(f".{link_html}/text()")
                if prop_sel:
                    item[prop['name']] = prop_sel[0].extract()
        yield item

    def _process_winner_li(self, winner_item: Selector, country=None) -> Dict[str, str | int]:
        """
        Process a winner's <li> tag, adding country of birth or nationality, as applicable.
        """
        text = ' '.join(winner_item.xpath('descendant-or-self::text()').extract())
        year = YEAR_PATTERN.findall(text)
        category = CATEGORY_PATTERN.findall(text)
        is_asteriks_contained = self._is_asteriks_contained(text)
        data = {
            # Get the href link-address from the <a> tag
            'link': BASE_URL + winner_item.xpath('a/@href').extract()[0],
            # Get comma-delineated name and strip trailing whitespace
            'name': text.split(',')[0].strip(),
            'year': int(year[0]) if year else None,
            'category': category[0] if category else None,
            'country': country if not is_asteriks_contained else None,
            'born_in': country if is_asteriks_contained else None,
            'text': text
        }
        return data

    @staticmethod
    def _is_asteriks_contained(text: str) -> bool:
        return True if text.find("*") >= 0 else False
