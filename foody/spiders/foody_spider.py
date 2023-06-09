# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider , Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
import time
from ..items import FoodyItem
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re

class FoodySpider(CrawlSpider):
	name = "foody"
	allowed_domains = [
		"www.foody.vn",
	]

	start_urls = [
		'http://www.foody.vn',
		'http://www.foody.vn/ha-noi/nha-hang'
	]

	__queue = [
		r'(.?)page=[23456789]'
	]

	rules = [
	    Rule(
	    	LinkExtractor(allow=(
	    		# r'[-\w]+\/',
	    		r'bo-suu-tap\/[-.?=\w\/]+',
	    		r'ha-noi\/[-.?=\w]+',
	    		r'ha-noi\/[-.?=\w]+\/',
	    	), deny=__queue,
	    	restrict_xpaths=[
	    		# r'//div[6]/section[1]/div/div/div/div[2]/div/div[3]',
	    		# r'//div[6]/section[1]/div/div/div/div[2]/div',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[1]/div/div/div[1]',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[3]/div/div/div/div[3]/div/div/div[3]/div',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[3]/div/div/div/div[3]/div/div/div[4]',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div',
	    		# r'//div[6]/section[2]/div/div/div/div/div[1]/div[4]/div/div'
	    	]), 
	    	callback='parse_extract_data_city', follow=True
	    	)
	    ]

	
	def extract(self,sel,xpath):
		try:
			data = sel.xpath(xpath).extract()
			text = filter(lambda element: element.strip(), data)
			return ''.join(text)
			# return re.sub(r"\s+", "", ''.join(text).strip(), flags=re.UNICODE)

		except Exception:
			raise Exception("Invalid XPath: %s" % e)


	def parse_extract_data_city(self, response):
		item = None
		try:
			if ('khu-vuc' not in response.url) and ('bo-suu-tap' not in response.url):
				sel = response
				item = FoodyItem()
				item['url'] = response.url
				item['title'] = response.css('title::text').extract()
				item['address'] = " ".join(response.css('div.res-common-add span::text')[1].getall() + response.css('div.res-common-add span::text')[3].getall() + response.css('div.res-common-add span::text')[4].getall())
    # lane = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[1]/div[3]/div/div[2]/div[1]//text()')
    # city = self.extract(sel,'//text()')
    # phone = self.extract(sel,'//text()')
				item['time_start'] = " ".join(response.css('div.micro-timesopen>span:nth-child(3)::text').getall()).split(" - ")[0].replace('\xa0', '')
				item['time_end'] = " ".join(response.css('div.micro-timesopen>span:nth-child(3)::text').getall()).split("- ")[1]
				item['price_start']= response.css('div.res-common-minmaxprice>span:nth-child(2)>span::text').get().split("-")[0]
				item['price_end'] = response.css('div.res-common-minmaxprice>span:nth-child(2)>span>span::text').get()
				item['image'] = response.css('img.pic-place::attr(src)').getall()
				
				#item['total_write_review'] = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/div[1]/ul/li[1]/a[2]/span//text()')
				#item['total_upload_images'] = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/div[1]/ul/li[2]/a[2]/span//text()')
				#item['total_check_in'] = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/div[1]/ul/li[3]/a[2]/span//text()')
				#item['total_save_to_love_collection'] = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/div[1]/ul/li[4]/a[2]/span//text()')
				#item['total_save_to_wish_collection'] = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/div[1]/ul/li[5]/a[2]/span//text()')
				#item['total_save_to_custom_collections'] = self.extract(sel,'//section[1]/div/div/div/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/div[1]/ul/li[6]/a[2]/span//text()')

				item['score_space'] = response.css('div.microsite-point-group>div:nth-child(5)>div>span::text').getall()
				item['score_quality'] = response.css('div.microsite-point-group>div:nth-child(3)>div>span::text').getall()
				item['score_price'] = response.css('div.microsite-point-group>div:nth-child(2)>div>span::text').getall()
				item['score_service'] = response.css('div.microsite-point-group>div:nth-child(4)>div>span::text').getall()
				item['score_location'] = response.css('div.microsite-point-group>div:nth-child(1)>div>span::text').getall()

				item['total_score_comment_for_excellent'] = ' '.join(response.css('b.exellent::text').getall()).strip()
				item['total_score_comment_for_good'] = ' '.join(response.css('b.good::text').getall()).strip()
				item['total_score_comment_for_avg'] = ' '.join(response.css('b.average::text').getall()).strip()
				item['total_score_comment_for_bad'] = ' '.join(response.css('b.bad::text').getall()).strip()
				item['avg_score_comment'] = ' '.join(response.css('div.ratings-boxes-points>div>span>b::text').getall()).strip()
				
				#geo = self.extract(sel,'//a[@class="linkmap"]/img/@src').split('_')
				#item['geo_latitude'] = geo[-2].replace('-','.')
				#item['geo_longitude'] = geo[-1].replace('-','.').replace('.jpg','')

				#item['types'] = self.extract(sel,'//div[@class="new-detail-info-sec"][2]/div[1]/div[2]//text()')
				#item['dining_time'] = self.extract(sel,'//div[@class="new-detail-info-sec"][1]/div[2]/div[2]//text()')
				#item['last_order'] = self.extract(sel,'//div[@class="new-detail-info-sec"][1]/div[3]/div[2]//text()')
				#item['waiting_time'] =self.extract(sel,'//div[@class="new-detail-info-sec"][1]/div[4]/div[2]//text()')
				#item['holiday'] = self.extract(sel,'//div[@class="new-detail-info-sec"][1]/div[5]/div[2]//text()')
				#item['capacity'] = self.extract(sel,'//div[@class="new-detail-info-sec"][2]/div[2]/div[2]//text()')
				#item['cuisine_style']  = self.extract(sel,'//div[@class="new-detail-info-sec"][2]/div[3]/div[2]//text()')
				#item['good_for'] = self.extract(sel,'//div[@class="new-detail-info-sec"][2]/div[4]/div[2]//text()')
				#item['typical_dishes']  = self.extract(sel,'//div[@class="new-detail-info-sec"][2]/div[5]/div[2]//text()')
				#item['website'] = self.extract(sel,'//div[@class="new-detail-info-sec"][3]/div/div[2]//b/text()')

				#item['is_reservation_required'] = self.extract(sel,'//ul[@class="micro-property"]/li[1]/@class') or True
				#item['is_delivery_service'] = self.extract(sel,'//ul[@class="micro-property"]/li[2]/@class') or True
				#item['is_takeaway_service'] = self.extract(sel,'//ul[@class="micro-property"]/li[3]/@class') or True
				#item['is_wifi'] =self.extract(sel,'//ul[@class="micro-property"]/li[4]/@class') or True
				#item['is_playground_for_kid'] = self.extract(sel,'//ul[@class="micro-property"]/li[5]/@class') or True
				#item['is_outdoor_seat'] = self.extract(sel,'//ul[@class="micro-property"]/li[6]/@class') or True
				#item['is_private_room'] = self.extract(sel,'//ul[@class="micro-property"]/li[7]/@class') or True
				#item['is_air_conditioner'] = self.extract(sel,'//ul[@class="micro-property"]/li[8]/@class') or True
				#item['is_credit_card_available'] = self.extract(sel,'//ul[@class="micro-property"]/li[9]/@class') or True
				#item['is_karaoke_service'] = self.extract(sel,'//ul[@class="micro-property"]/li[10]/@class') or True
				#item['is_free_bike_park'] = self.extract(sel,'//ul[@class="micro-property"]/li[11]/@class') or True
				#item['is_tip_for_staff'] = self.extract(sel,'//ul[@class="micro-property"]/li[12]/@class') or True
				#item['is_car_park'] = self.extract(sel,'//ul[@class="micro-property"]/li[13]/@class') or True
				#item['is_smoking_zone'] = self.extract(sel,'//ul[@class="micro-property"]/li[14]/@class') or True
				#item['is_member_card'] = self.extract(sel,'//ul[@class="micro-property"]/li[15]/@class') or True
				#item['is_tax_invoice_available'] = self.extract(sel,'//ul[@class="micro-property"]/li[16]/@class') or True
				#item['is_conference_support'] = self.extract(sel,'//ul[@class="micro-property"]/li[17]/@class') or True
				#item['is_heat_conditioner'] = self.extract(sel,'//ul[@class="micro-property"]/li[18]/@class') or True
				#item['is_disabled_person_support'] = self.extract(sel,'//ul[@class="micro-property"]/li[19]/@class') or True
				#item['is_live_sport_tv'] = self.extract(sel,'//ul[@class="micro-property"]/li[20]/@class') or True
				#item['is_live_music'] = self.extract(sel,'//ul[@class="micro-property"]/li[21]/@class') or True
		except:
			pass

		if (item and ('title' in item and item['title'] != '') and ( 'address' in item and item['address'] != '[]' and item['address'] != "") and ('time_start' in item and item['time_start']!='[]')
		    and ('score_space' in item and item['score_space'] != '[]') and ('avg_score_comment' in item and item['avg_score_comment']!="")) :
			yield item