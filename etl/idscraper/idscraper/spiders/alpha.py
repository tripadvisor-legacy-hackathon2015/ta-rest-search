# -*- coding: utf-8 -*-
import scrapy
import re
from idscraper.items import AlphaItem
class AlphaSpider(scrapy.Spider):
    name = "alpha"
    allowed_domains = ["tripadvisor.ca","*"]
    start_urls = [ "http://www.tripadvisor.ca/Restaurants-g155004-Ottawa_Ontario.html" ]

    def parse(self, response):
        for restaurant in response.xpath('//div[@id="EATERY_SEARCH_RESULTS"]//a[@class="property_title"]'):
            item = AlphaItem()
            print restaurant
            item['name']=restaurant.xpath('text()').extract()
            item['url']=restaurant.xpath('@href').extract()
            item['id']= restaurant.xpath('@href').re('.*-d([\d]{7})-.*')
            #  <a target="_blank" href="/Restaurant_Review-g2690985-d4494962-Reviews-Wiches_Cauldron-Stittsville_Ottawa_Ontario.html" class="property_title" onclick="ta.restaurant_list_tracking.clickDetailTitle('/Restaurant_Review-g2690985-d4494962-Reviews-Wiches_Cauldron-Stittsville_Ottawa_Ontario.html','tags_category_tag_restaurants','4494962','1','46');">
            #  'Wiches Cauldron
            #  </a>'
            print item
            yield item
        pass
