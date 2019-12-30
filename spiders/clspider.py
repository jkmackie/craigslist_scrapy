# -*- coding: utf-8 -*-
import scrapy

#scrape with this terminal command:  scrapy crawl clspider -o mycity.json
#scrapy version = 1.60.  Shift + Alt + F to format JSON in VS Code.

class ClspiderSpider(scrapy.Spider):
    name = 'clspider'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://elpaso.craigslist.org/search/cta?auto_make_model=ford']  #cta is cars + trucks by ALL
    base_url = 'https://elpaso.craigslist.org'
    
    #Get all the vehicle_url    
    def parse(self, response):
        all_vehicles = response.xpath('//li[@class="result-row"]')
        
        for vehicle in all_vehicles:
            vehicle_url = vehicle.xpath('.//a/@href').extract_first()
            yield scrapy.Request(vehicle_url, callback=self.parse_vehicle)
        
        next_page_partial_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse)

     #Parse the vehicle_url data 
    def parse_vehicle(self, response):
        url_vehicle = response.url
        print("####URL_VEHICLE", url_vehicle)
        title = response.xpath('//span[@id="titletextonly"]/text()').extract_first()
        price = response.xpath('//span[@class="price"]/text()').extract_first()
        subLocation = response.xpath('//span[@class="price"]/following-sibling::small/text()').extract_first()
        body = response.xpath('//section[@id="postingbody"]/text()').extract()
        attribDict={}
        for i in range(0,len(response.xpath('//p[@class="attrgroup"]/span/b').extract())):
            attribDict[i] = response.xpath('//p[@class="attrgroup"]/span').extract()[i]

        imageDict={}
        for i in range(0, len(response.xpath('//div[@id="thumbs"]/a/@href').extract())):
            imageDict[i] = response.xpath('//div[@id="thumbs"]/a/@href').extract()[i]
        yield {
            'URL_Vehicle' : url_vehicle,
            'Title' : title,
            'Price' : price,
            'SubLoc' : subLocation,
            'Body' : body,
            'AttribDictionary' : attribDict,
            'ImageDictionary' : imageDict
        }
