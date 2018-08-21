# -*- coding: utf-8 -*-
import scrapy
import pickle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AthleteSpider(scrapy.Spider):
    name = "athlete"
    allowed_domains = ["athletic.net"]
    DOWNLOAD_DELAY = 0.3
    start_urls = (
        'http://www.athletic.net/', 'http://www.athletic.net/TrackAndField/College/','http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=70513',
    )
    rules = (Rule(LinkExtractor(allow=()), callback='parse', follow=True),)
    max_cid = 36
    max_page = 55
    
    def closed(self,reason):
		pickle.dump(self.athletes, open('athletes.lst','wb'))	
    def start_requests(self):
		self.athletes = list()
		
		starturls = [
		'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=70513&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=59489&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=49375&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=43109&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=32304&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=27991&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=17228&Event='
		,'http://www.athletic.net/TrackAndField/Division/Event.aspx?DivID=10057&Event='
		
		
		
		]
		
		
		

		
			
		for i in range(self.max_cid):
			for j in range(self.max_page):
				for url in starturls:
					yield scrapy.Request(url+str(i)+"&page="+str(j),callback=self.parse)
   
    def parse(self, response):
		for link in LinkExtractor(allow=self.allowed_domains).extract_links(response):
			print(link.url)
			if 'Athlete' in link.url and link.url not in self.athletes:
				self.athletes.append(link.url)
	
        
