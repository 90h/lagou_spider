# coding: utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector


class SecooSpider(Spider):
    name = 'lg_spider'

    start_urls = [
        'https://www.lagou.com/zhaopin/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            self.logger.warning(u'\n\n' + u'go =>>> :' + url + u'\n')
            yield Request(url=url, callback=self.parse, headers={'Referer': url})

    def parse(self, response):
        selector = Selector(response)
        items = selector.xpath(
            'body/div[@id="content-container"]/div[@id="main_container"]/'
            'div[@class="content_left"]/div[@id="s_position_list"]/'
            'ul[@class="item_con_list"]/li')
        for item in items:
            position = item.xpath('div[@class="list_item_top"]/div[@class="position"]/'
                                  'div[@class="p_top"]/a/h2/text()').extract_first().strip()
            address = item.xpath('div[@class="list_item_top"]/div[@class="position"]/'
                                 'div[@class="p_top"]/a/span/em/text()').extract_first().strip()
            money = item.xpath('div[@class="list_item_top"]/div[@class="position"]/'
                               'div[@class="p_bot"]/div[@class="li_b_l"]/'
                               'span/text()').extract_first().strip()
            requirements = item.xpath('div[@class="list_item_top"]/div[@class="position"]/'
                                      'div[@class="p_bot"]/'
                                      'div[@class="li_b_l"]').extract_first().split('-->')[1][0:-6].strip()
            company = item.xpath('div[@class="list_item_top"]/div[@class="company"]/'
                                 'div[@class="company_name"]/a/text()').extract_first()
            industry = item.xpath('div[@class="list_item_top"]/div[@class="company"]/'
                                  'div[@class="industry"]/text()').extract_first().strip()

            with open('lagou.txt', 'a') as f:
                f.write('职位: ' + position + '\n'
                        + '地址: ' + address + '\n'
                        + '薪资: ' + money + '\n'
                        + '需求: ' + requirements + '\n'
                        + '公司: ' + company + '\n'
                        + '行业: ' + industry + '\n\n\n')

        next_page = selector.xpath(
            'body/div[@id="content-container"]/div[@id="main_container"]/'
            'div[@class="content_left"]/div[@id="s_position_list"]/'
            'div[@class="item_con_pager"]/div[@class="pager_container"]/a[last()]/@href').extract_first()

        if next_page != u'javascript:;':
            self.logger.warning(u'\n\n' + u'go =>>> :' + next_page + u'\n')
            yield Request(url=next_page, callback=self.parse, headers={'Referer': response.url})
        else:
            self.logger.warning(u'\n\n' + u'die!' + u'\n')
