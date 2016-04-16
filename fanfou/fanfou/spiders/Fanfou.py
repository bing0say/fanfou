#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'jiang'
__creattime__ = '2016/3/6 20:35'

import scrapy
from scrapy.dupefilter import RFPDupeFilter
from fanfou.settings import PASSNAME,PASSWORD
from fanfou.items import FanfouItem
from scrapy.http import Request

class NullDupeFilter(RFPDupeFilter):
    def request_seen(self, request):
        return False


class FanfouSpider(scrapy.Spider):
    name = 'fanfou'
    start_urls = ['http://fanfou.com']

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                    formdata ={'loginname':PASSNAME,'loginpass':PASSWORD},
                    callback = self.login_after,
                    method = 'POST',
                    )

    def login_after(self,response):
        for i in range(1,119):
            p = 'p.' + str(i)
            # return scrapy.Request('http://fanfou.com/~RLhcIDBjZAM/'+p,self.parse_index)
            detail_url = "http://fanfou.com/~RLhcIDBjZAM/" + p
            req = Request(detail_url,self.parse_index)
            item = FanfouItem()
            req.meta['item'] = item
            yield req
    def parse_index(self,response):
        # print response.body
        # item = FanfouItem()
        item = response.meta['item']
        dic = []
        for content in response.xpath("//div[@id='content']"):
            time= content.xpath(".//span[@class='stamp']/a/text()").extract()
            contents= content.xpath(".//span[@class='content']/text()").extract()
            if contents and contents not in dic:
                dic.append({'time':time,'contents':contents})
                item['dic'] = dic
                yield item
