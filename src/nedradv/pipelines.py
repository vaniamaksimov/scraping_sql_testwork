# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter

from src.core.database import db_session


class NedradvPipeline:
    async def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        await db_session()
        parsed_item = ItemAdapter(item)
        parsed_item
        print('*' * 50)
        print('PIPELINE')
        print('*' * 50)
        return item
