import scrapy
import re
import json

class collect_car_info(scrapy.Spider):
	name='cars_info'

	def __init__(self):
		try:
			with open('dataset/cars_urls.json') as f:
				self.cars = json.load(f)
				self.car_count = 1
		except IOError:
			print("File not found")

	def start_requests(self):
		urls = ['https://www.autotrader.com.au' + self.cars[self.car_count-1]['car_url']]
		# YOUR CODE HERE

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
		
	def parse(self, response):
		# YOUR CODE HERE
		cars = response.css('.content')
		for car in cars:
			car_id = self.cars[self.car_count-1]['car_url']
			car_id = re.findall('\d+', car_id)[0]
			car_name = car.xpath('//h1[@class="title"]/text()').get().replace('\n','').strip()


			car_price = car.xpath('//div[@class="tabs--slider"]//div[1]//div//table//tbody//tr[3]//td[2]/text()').get().replace('\n','').strip()
			car_kinds = car.xpath('//div[@class="tabs--slider"]//div[3]//div[1]//div[6]//table//tbody//tr//td[2]/text()').getall()[0:4]
			car_kinds = [item.replace('\n','').strip() for item in car_kinds]
			car_year = re.findall('^\d+', car_name)[0]
			
			car_details = car.xpath('//div[@class="vehicleDetails--details"]//div//div/text()').getall()[0:5]
			car_details = [item.replace('\n','').strip() for item in car_details]
			car_details[2] = re.findall('\w+', car_details[2])[0]
			car_details[4] = re.findall('[^:]+', car_details[4])[1]
			
			car_cc = car.xpath('//div[@class="tabs--slider"]//div[3]//div[1]//div[4]//table//tbody//tr[2]//td[2]/text()').get().replace('\n','').strip()
			
			car_color = car.xpath('//div[@class="tabs--slider"]//div[1]//div[1]//table//tbody//tr[10]//td[2]/text()').get().replace('\n','').strip()
			if car_color != '- / -':
				car_color = re.findall('\w+', car_color)[0]
			else:
				car_color = ''
			
			car_seat = car.xpath('//div[@class="tabs--slider"]//div[3]//div[1]//div[2]//table//tbody//tr//td[2]/text()').get().replace('\n','').strip()


			
			car_dict = {
				'ID': car_id,
				'Name': car_name,
				'Price': car_price,
				'Brand': car_kinds[0],
				'Model': car_kinds[1],
				'Variant': car_kinds[2],
				'Series': car_kinds[3],
				'Year': car_year,
				'Kilometers': car_details[0],
				'Type': car_details[1],
				'Gearbox': car_details[2],
				'Fuel': car_details[3],
				'Status': car_details[4],
				'CC': car_cc,
				'Color': car_color,
				'Seating Capacity': car_seat,
			}

			yield car_dict


			if self.car_count < len(self.cars):
				next_page_url = 'https://www.autotrader.com.au' + self.cars[self.car_count]['car_url']
				self.car_count += 1
				yield scrapy.Request(url=next_page_url, callback=self.parse) 