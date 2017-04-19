# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhilianItem(Item):
    job_name = Field()
    firm_name = Field()
    salary = Field()
    working_place = Field()
    pub_date = Field()
    firm_size = Field()
    work_requirement = Field()
    job_describe = Field()
    link = Field()
