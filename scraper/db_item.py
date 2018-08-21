from pymongo import MongoClient
from datetime import datetime
class Athlete:
	def __init__(self, athlete_id, name):
			self.name = name
			self.athlete_id = athlete_id
			self.seasons = []
	def add_season(self, event):
		self.seasons.append(event)
	
			
class Season:
	def __init__(self, school, season):
			

		self.season = season

		self.school = school
		self.events = []
	def add_event(self, event):
		self.events.append(event)
	
class DBItem:
	##Add class to hold arrays
	##Convert Date String to datetime
	##Add Athlete class and season class

	def __init__(self, event):
		
		
		self.event = event
		
		self.times = []
		self.days = []
		self.meet = []
		
	def add_time(self, time):
		self.times.append(time)
	def add_day(self,day):
		#self.days.append(str(datetime.strptime(day,"%b %d")))
		self.days.append(day)

	def add_meet(self, meet):
		self.meet.append(meet)
		
