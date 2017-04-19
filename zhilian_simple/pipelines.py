# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.utils.log import configure_logging

class ZhilianPipeline(object):
    def __init__(self):
        #self.file = codecs.open('dangd_book.json', mode = 'wb', encoding = 'utf-8')
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        #line = json.dumps(dict(item)) + '\n'
        #self.file.write(line.decode('unicode_escape'))
        self.collection.insert(dict(item))
        return item
