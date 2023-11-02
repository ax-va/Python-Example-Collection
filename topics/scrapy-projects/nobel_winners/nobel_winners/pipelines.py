# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class NobelWinnersPipeline:
    def process_item(self, item, spider):
        return item


class DroppingNonPersons:
    """
    Removes non-person Nobel Prize winners.
    """
    def process_item(self, item, spider):
        if not item.get('gender'):
            item_name = item['name']
            raise DropItem(f"No gender for '{item_name}'")
        return item


class NobelPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [img['path'] for ok, img in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item
