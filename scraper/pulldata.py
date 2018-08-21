import pymongo
import pprint
import re
from datetime import datetime
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.db
collection = db.athletes
f1 = open('data.txt','w')
f2 = open('labels.txt','w')
for i in collection.find({'seasons.events.event':'100 Meters'},{'seasons.season':1, 'seasons.events.times':1 ,'seasons.events.days':1, 'seasons.events.event':1, '_id':0}):
	 for y in i['seasons']:
		 if '' in y['season']:
			 
			 for j in y['events']:
				 if '100 Meters' in j['event']:
					 if 'DNS' not in j['times'] and 'FS' not in j['times'] and 'DQ' not in j['times'] and 'DNF' not in j['times'] and 'SCR' not in j['times'] and 'NT' not in j['times']:
						year = y['season'].split(" ")[0]
						
						pprint.pprint(y['season'])
						s = ''
						if len(j['days'])> 2:
							for k in j['days']:
								#time = year + ' ' + k
								time = year + ' ' + k.replace(' ','')
								#s += str(datetime.strptime(time,"%Y %b %d").strftime('%s')) + ','
								s += (k.replace(" ","/") + ',')
								#s += year + (re.sub(r'[0-9]','',time)+",")
							s = s[:-1]
							f2.write(s + '\n')
						s = ''
						if len(j['times'])> 2:
							for k in j['times']:
								s += (re.sub(r'[A-Za-z]','',k)+",")
								#s += k +",";

							s = s[:-1]
							f1.write(s + '\n')
							pprint.pprint(j['event'])
