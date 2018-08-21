from lxml import html
import requests
import jsonpickle
import re
from bs4 import BeautifulSoup
import urllib2
import pickle
from db_item import DBItem, Athlete, Season
from database_client import DatabaseClient
import sys
import json
def jdefault(o):
    return o.__dict__
def parseAthlete(url):
	try:
		client = DatabaseClient()
		client.connect("localhost",27017)
		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page.read(), "lxml")
		div = soup.findAll("div", { "class" : "L8" })
		athlete_id = url.replace("http://www.athletic.net/TrackAndField/Athlete.aspx?AID=","")
		name = soup.find("h2",{"class":"mTop10"})
		school = soup.find("h1",{"class":"mTop10"})
		name = name.contents[1]
		school = school.a.contents[0]
		athlete = Athlete(athlete_id, name)
		for i in div:
			season = i.h4.span.contents[0]
			season_obj = Season(str(school), season)
			print(season)
			panel = i.findAll("div", { "class" : "panel-body" })
			for j in panel:
				h5 = j.findAll('h5') 
				table = j.findAll("tbody")
				for y in range(0,len(table)):
					event = h5[y].contents[0]
					print(event)
					db_item = DBItem(str(event))
					tr = table[y].findAll("tr")
					for l in tr:
						td = l.findAll("td")
						for x in range(len(td)):
							if td[x].find('a') != None:
								string = td[x].find('a').contents[0]
								if "<i" not in str(string):
									print(string)
									if x == 1:
										db_item.add_time(str(string))
									elif x == 2:
										db_item.add_day(str(string))
									elif x == 3:
										db_item.add_meet(str(string))
							elif td[x].find('i') != None:
								string = td[x].find('i').contents[0]
								
								print(string)
								if x == 1:
									db_item.add_time(str(string))
								elif x == 2:
									db_item.add_day(str(string))
								elif x == 3:
									db_item.add_meet(str(string))
							else:
								string = td[x].contents[0]
								print(string)
								if x == 1:
									db_item.add_time(str(string))
								elif x == 2:
									db_item.add_day(str(string))
								elif x == 3:
									db_item.add_meet(str(string))
					season_obj.add_event(db_item)
			athlete.add_season(season_obj)
		
		strn = json.dumps(athlete, default=jdefault)
		
		client.insert(json.loads(strn))
	except:
		print("error")
					
			
			
lst = file('../Spider/athletes.lst','rb')
lst = pickle.load(lst)	
sys.setrecursionlimit(100000)
for i in lst:		
	parseAthlete(i)
