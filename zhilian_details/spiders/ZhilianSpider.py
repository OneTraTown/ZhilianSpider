# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from ..items import ZhilianItem
from  scrapy.http import Request

class ZhilianSpider(CrawlSpider):
    name = 'ZhilianSpider'
    allow_domains = ['sou.zhaopin.com']
    work_place = ['全国']  #'北京','上海','广州','深圳'
    job_name = ['Python'] # ,'Java','数据挖掘','爬虫','数据分析'
    start_urls = []
    for place in work_place:
        for job in job_name:
            urls = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=' + str(place) + '&kw=' + str(job)
            start_urls.append(urls)

    #start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=python&p=1']
    rules = (
        Rule(LinkExtractor(allow=(r'&p=[1-9]$',r'&p=[1-3][0-9]$'),deny=(r'&p=\d{3}')),
         callback = 'parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        link_list = sel.xpath('//td[@class="zwmc"]/div/a/@href').extract()
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
        #Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        while(link_list):
            try:
                urls = link_list.pop()
                yield Request(url = urls,headers = headers, method = 'GET' , callback = self.parse_details)
            except:
                pass

    def parse_details(self, response):
        sel = Selector(response)
        item = ZhilianItem()

        try:
            item['link'] = response.url   #str(response.url)
            item['job_name'] = sel.xpath('/html/body/div[5]/div[1]/div[1]/h1/text()').extract()[0]
            item['firm_name'] = sel.xpath('/html/body/div[5]/div[1]/div[1]/h2/a/text()').extract()[0]
            item['welfare'] = sel.xpath('/html/body/div[5]/div[1]/div[1]/div[1]').xpath('string(.)').extract()[0]
            item['salary'] = sel.xpath('/html/body/div[6]/div[1]/ul/li[1]').xpath('string(.)').extract()[0][5:]
            item['work_place'] = sel.xpath('/html/body/div[6]/div[1]/ul/li[2]').xpath('string(.)').extract()[0][5:]
            item['pub_date'] = sel.xpath('/html/body/div[6]/div[1]/ul/li[3]').xpath('string(.)').extract()[0][5:]
            item['work_require'] = sel.xpath('/html/body/div[6]/div[1]/ul/li[5]').xpath('string(.)').extract()[0][5:]
            item['edu_require'] = sel.xpath('/html/body/div[6]/div[1]/ul/li[6]').xpath('string(.)').extract()[0]
            item['job_category'] = sel.xpath('/html/body/div[6]/div[1]/ul/li[8]').xpath('string(.)').extract()[0][5:]
            item['firm_size'] = sel.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[1]').xpath('string(.)').extract()[0][5:]
            item['firm_trade'] = sel.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[3]').xpath('string(.)').extract()[0][5:]
            item['firm_url'] = sel.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[4]/strong/a/text()').extract()[0]
            item['firm_addr'] = sel.xpath('/html/body/div[6]/div[2]/div[1]/ul/li[5]/strong/text()').extract()[0][5:].strip()
            details = ''
            divs = sel.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]')
            count = 0
            for p in divs.xpath('//p/text()'):
                if count > 10 :
                    break
                details += p.extract().strip()
                count += 1
            item['details'] = details

        except:
            pass

        return item
