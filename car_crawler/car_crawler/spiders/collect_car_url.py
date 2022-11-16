import scrapy

class collect_car_url(scrapy.Spider):
	name = 'cars_urls'

	def __init__(self):
		self.start = 1
	
	def start_requests(self):
		urls = ['https://www.autotrader.com.au/for-sale?page=1']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		
		for item in response.css('section.row a.carListing'):
			yield {
				'car_url': item.css('a.carListing::attr(href)').get(),
			}

		if self.start < 6081:
			self.start += 1

			next_page_url = 'https://www.autotrader.com.au/for-sale?page=' + f'{self.start}'
			yield scrapy.Request(url=next_page_url)