# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from ..items import ZhilianItem


class ZhilianSpider(CrawlSpider):
    name = 'ZhilianSpider'
    allow_domains = ['sou.zhaopin.com']
    work_place = ['全国'] #'北京','上海','广州','深圳'
    job_name = ['Python'] #'Java','数据挖掘','爬虫','数据分析',
    start_urls = []
    for place in work_place:
        for job in job_name:
            urls = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + str(place) + '&kw=' + str(job)
            start_urls.append(urls)

    #start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=python&p=1']
    rules = (
        Rule(LinkExtractor(allow=(r'&p=[1-9]$', r'&p=[1-3][0-9]$')),
         callback = 'parse_item', follow=True),
    )

    def parse_item(self, response):
        items = []
        sel = Selector(response)

        name_list = sel.xpath('//td[@class="zwmc"]/div/a').xpath('string(.)').extract()
        link_list = sel.xpath('//td[@class="zwmc"]/div/a/@href').extract()
        firm_list = sel.xpath('//td[@class="gsmc"]/a').xpath('string(.)').extract()
        salary_list = sel.xpath('//td[@class="zwyx"]').xpath('string(.)').extract()
        workplace_list = sel.xpath('//td[@class="gzdd"]').xpath('string(.)').extract()
        pubdate_list = sel.xpath('//td[@class="gxsj"]/span/text()').extract()
        firmsize_list = sel.xpath('//li[@class="newlist_deatil_two"]/span[3]/text()').extract()
        workreq_list = sel.xpath('//li[@class="newlist_deatil_two"]/span[4]/text()').extract()
        details_list =  sel.xpath('//li[@class="newlist_deatil_last"]').xpath('string(.)').extract()
        while(name_list):
            item = ZhilianItem()
            try:
                item['job_name'] = name_list.pop()
                item['link'] = link_list.pop()
                item['firm_name'] = firm_list.pop()
                item['salary'] = salary_list.pop()
                item['working_place'] = workplace_list.pop()
                item['pub_date'] = pubdate_list.pop()
                item['firm_size'] = firmsize_list.pop()
                item['work_requirement'] = edureq_list.pop()
                item['job_describe'] = details_list.pop()
            except:
                pass
            items.append(item)
        return items
