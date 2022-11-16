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
		urls = ['https://www.autotrader.com.au/car/12817873/renault/arkana/nsw/narellan/suv']
		# YOUR CODE HERE

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
		
	def parse(self, response):
		# YOUR CODE HERE
		cars = response.css('.info')
		for car in cars:
			car_id = car.xpath('//div[@class="card" and h5="Profile"]//li[label = "ID"]/text()').extract_first()
			car_name = car.css('div.info h1::text').get()

			car_positions = car.xpath('//div[@class="info"]//span/text()').extract()
			car_primary_position = car.xpath('//div[@class="center"]//div//div//ul//li[label="Best Position"]//span/text()').get()

			car_info = car.xpath('//div[@class="meta ellipsis"]/text()').getall()
			car_info = [info for info in car_info if info != ' ']
			car_info = ''.join(car_info)

			car_age = re.findall("\d+",car_info)[0]
			car_height = re.findall("\d+",car_info)[3]
			car_weight = re.findall("\d+",car_info)[4]
			car_birthday_month = re.findall("[a-z|A-Z]+",car_info)[2]
			car_birthday_day = re.findall("\d+",car_info)[1]
			car_birthday_year = re.findall("\d+",car_info)[2]
			car_birthday = car_birthday_year + "/" + car_birthday_month + "/" + car_birthday_day

			car_stats = car.xpath('//div[@class="sub"]/text()').getall()
			car_stats_values = car.xpath('//section[@class="card spacing"]/div/div/span[not (@class="plus" or @class="minus")]/text()').getall()
			car_stats_values = car_stats_values + [stat for stat in car.xpath('//section[@class="card spacing"]/div/div/text()').getall() if stat != ' ']
			stats = {u:v for u,v in zip(car_stats, car_stats_values)}
			stats["Overall Rating"] = int(stats["Overall Rating"])
			stats["Potential"] = int(stats["Potential"])

			car_profile_stats = car.xpath('//div[@class="card" and h5="Profile"]//label/text()').getall()
			car_profile_values = car.xpath('//div[@class="card" and h5="Profile"]//li[label != "ID"]/text()').getall()
			car_profile_values = [u for u in car_profile_values if u != ' ']
			car_profile_values = car_profile_values + car.xpath('//div[@class="card" and h5="Profile"]//li//span[not (@class)]/text()').getall()
			profiles = {u:v for u,v in zip(car_profile_stats, car_profile_values)}
			profiles["Weak Foot"] = int(profiles["Weak Foot"])
			profiles["Skill Moves"] = int(profiles["Skill Moves"])
			profiles["International Reputation"] = int(profiles["International Reputation"])

			car_teams = car.xpath('//div[@class="card"]//h5//a/text()').getall()
			car_teams_values = car.xpath('//div[@class="card"]//ul[@class="ellipsis pl"]//li[1]//span[1]/text()').getall()
			teams = {'teams':{u:int(v) for u, v in zip(car_teams, car_teams_values)}}

			car_attacking = car.xpath('//div[@class="card" and h5="Attacking"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_attacking = [ele.replace(" ","") for ele in car_attacking]
			car_attacking_values = car.xpath('//div[@class="card" and h5="Attacking"]//ul//li//span[1]/text()').getall()
			attacking = {'attacking':{u:int(v) for u,v in zip(car_attacking, car_attacking_values)}}

			car_skill = car.xpath('//div[@class="card" and h5="Skill"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_skill = [ele.replace(" ","") for ele in car_skill]
			car_skill_values = car.xpath('//div[@class="card" and h5="Skill"]//ul//li//span[1]/text()').getall()
			skill = {'skill':{u:int(v) for u,v in zip(car_skill, car_skill_values)}}

			car_movement = car.xpath('//div[@class="card" and h5="Movement"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_movement = [ele.replace(" ","") for ele in car_movement]
			car_movement_values = car.xpath('//div[@class="card" and h5="Movement"]//ul//li//span[1]/text()').getall()
			movement = {'movement':{u:int(v) for u,v in zip(car_movement, car_movement_values)}}

			car_power = car.xpath('//div[@class="card" and h5="Power"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_power = [ele.replace(" ","") for ele in car_power]
			car_power_values = car.xpath('//div[@class="card" and h5="Power"]//ul//li//span[1]/text()').getall()
			power = {'power':{u:int(v) for u,v in zip(car_power, car_power_values)}}

			car_mentality = car.xpath('//div[@class="card" and h5="Mentality"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_mentality = [ele.replace(" ","") for ele in car_mentality]
			car_mentality_values = car.xpath('//div[@class="card" and h5="Mentality"]//ul//li//span[1]/text()').getall()
			mentality = {'mentality':{u:int(v) for u,v in zip(car_mentality, car_mentality_values)}}

			car_defending = car.xpath('//div[@class="card" and h5="Defending"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_defending = [ele.replace(" ","") for ele in car_defending]
			car_defending_values = car.xpath('//div[@class="card" and h5="Defending"]//ul//li//span[1]/text()').getall()
			defending = {'defending':{u:int(v) for u,v in zip(car_defending, car_defending_values)}}

			car_goalkeeping = car.xpath('//div[@class="card" and h5="Goalkeeping"]//ul//li//span[@role="tooltip"]/text()').getall()
			car_goalkeeping = [ele.replace(" ","") for ele in car_goalkeeping]
			car_goalkeeping_values = car.xpath('//div[@class="card" and h5="Goalkeeping"]//ul//li//span[1]/text()').getall()
			goalkeeping = {'goalkeeping':{u:int(v) for u,v in zip(car_goalkeeping, car_goalkeeping_values)}}

			car_traits = car.xpath('//div[@class="card" and h5="Traits"]//ul//li//span/text()').getall()
			traits = {'car_traits': car_traits}

			car_special = car.xpath('//div[@class="card" and h5="car Specialities"]//ul//li//a/text()').getall()
			specialities = {'car_specialities': car_special}

			car_dict = {
				'id': car_id,
				'name': car_name,
				'primary_position': car_primary_position,
				'positions': car_positions,
				'age': car_age,
				'birth_date': car_birthday,
				'height': car_height,
				'weight': car_weight,
			}
			car_dict.update(stats)
			car_dict.update(profiles)
			car_dict.update(teams)
			car_dict.update(attacking)
			car_dict.update(skill)
			car_dict.update(movement)
			car_dict.update(power)
			car_dict.update(mentality)
			car_dict.update(defending)
			car_dict.update(goalkeeping)
			car_dict.update(traits)
			car_dict.update(specialities)

			yield car_dict


			if self.car_count < len(self.cars):
				next_page_url = 'https://www.autotrader.com.au' + self.cars[self.car_count]['car_url']
				self.car_count += 1
				yield scrapy.Request(url=next_page_url, callback=self.parse) 