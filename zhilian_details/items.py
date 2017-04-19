# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ZhilianItem(Item):
    job_name = Field()
    firm_name = Field()
    welfare = Field()
    salary = Field()
    work_place = Field()
    pub_date = Field()
    work_require = Field()
    edu_require = Field()
    job_category = Field()
    details = Field()
    firm_size = Field()
    firm_trade = Field()
    firm_url = Field()
    firm_addr = Field()
    link = Field()
