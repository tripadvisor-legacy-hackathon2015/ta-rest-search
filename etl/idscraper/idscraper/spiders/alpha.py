# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from idscraper.items import AlphaItem

class AlphaSpider(CrawlSpider):
    name = "alpha"
    allowed_domains = ["tripadvisor.ca","tripadvisor.com"]
    start_urls = [ "http://www.tripadvisor.ca/Restaurants-g155004-Ottawa_Ontario.html" ]

    #scrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//a[contains(concat(' ', normalize-space(@class), ' '), ' next')]"),allow=('.*',)),follow=True,callback='parse_item'),
    ) 

    def parse_item(self, response):
        self.logger.info('Parsing URL %s', response.url )
        for restaurant in response.xpath('//div[@id="EATERY_SEARCH_RESULTS"]//a[@class="property_title"]'):
            item = AlphaItem()
            #print restaurant
            item['name']=restaurant.xpath('text()').extract()
            item['url']=restaurant.xpath('@href').extract()
            item['id']= restaurant.xpath('@href').re('.*-d([\d]{1,9})-.*')
            #  print item
            #  print item['url']
            if not u'-g155004-' in str(item['url']):
                continue
            print str(item['id'][0])
            #  <a target="_blank" href="/Restaurant_Review-g2690985-d4494962-Reviews-Wiches_Cauldron-Stittsville_Ottawa_Ontario.html" class="property_title" onclick="ta.restaurant_list_tracking.clickDetailTitle('/Restaurant_Review-g2690985-d4494962-Reviews-Wiches_Cauldron-Stittsville_Ottawa_Ontario.html','tags_category_tag_restaurants','4494962','1','46');">
            #  'Wiches Cauldron
            #  </a>'
            yield item
        pass
