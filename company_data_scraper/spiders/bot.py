# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy import Request

class BotSpider(CrawlSpider):
    name = 'bot'
    allowed_domains = ['www.indiabusinesstoday.in']
    start_urls = ['http://www.indiabusinesstoday.in/category/architecture-interiors-1-1522']
    target_url = 'www.indiabusinesstoday.in/detail/'
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]
    def parse(self, response):
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        if self.target_url in response.url:
            data = {}
            data['Name Of Company'] = str(response.xpath("//div[@class='panel-heading']//span[@itemprop='name']//h1[@class='panel-title']/text()").extract_first()).strip()
            data['Contact Name'] = "None"
            stuff = response.xpath("//li[@class='list-group-item' and not(contains(@itemprop,'address'))]//span/text()").extract()
            for s in stuff:
                tmp = ""
                for char in str(s):
                    if char.isalpha():
                        tmp += char
                if tmp != "":
                    data['Contact Name'] = str(s).strip()
            data['Designation'] = "None"
            data['Street Address'] = str(response.xpath("//span[@itemprop='streetAddress']/text()").extract_first()).strip()
            if (data['Street Address'][-1] == ','):
                data['Street Address'] = data['Street Address'][:-1]
            data['City'] = str(response.xpath("//span[@itemprop='addressLocality']/text()").extract_first()).strip()
            data['State'] = str(response.xpath("//span[@itemprop='addressRegion']/text()").extract_first()).strip()
            data['Pincode'] = str(response.xpath("//li[@itemprop='address']/text()").extract_first()).strip().strip()
            data['Email'] = "None"
            data['Phone'] = str(response.xpath("//span[@itemprop='telephone']/text()").extract_first()).strip()

            tmp = ""
            for char in str(data['Phone']):
                if char.isalpha():
                    tmp += char
            if tmp != "":
                data['Contact Name'] = str(data['Phone'])
                data['Phone'] = 'None'

            data['Mobile'] =  str(response.xpath("//span[@itemprop='telephone']/text()").extract_first()).strip()
            data['Website'] = str(response.xpath("//a[@itemprop='url']/text()").extract_first()).strip()
            data['Employee Size'] = "None"
            yield data

        for link in links:
            is_allowed = False
            for allowed_domain in ['www.indiabusinesstoday.in/category/advertising', 'www.indiabusinesstoday.in/detail']:
                if allowed_domain in link.url:
                    is_allowed = True
            if is_allowed:
                yield Request(link.url, callback=self.parse)