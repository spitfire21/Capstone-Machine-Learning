from pymongo import MongoClient

class DatabaseClient:
	def __init__(self):
		client = MongoClient()

	def connect(self,url, port):
		client = MongoClient(url, port)
		self.db = client['db']
		self.collection = self.db['athletes']
	def insert(self,post):
		return self.collection.insert_one(post)
	def find(self,query):
		self.db.find_one(query)
	
