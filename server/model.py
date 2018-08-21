import json
import numpy as np
import keras
import base64
import math
from math import trunc
from keras.models import load_model

size = 128
class Model():
	results = list()

	def get_model(self):
		return json.dumps(self.results.tolist())
	def load_model(self):

		self.x = np.load(open('athletearray.tx','r'))
		#self.x2 = np.load(open('athletearray.tx','r'))
		self.y = np.load(open('athleteresults.tx','r'))

		self.model = load_model('100Mmodel.h5')
		self.MSE = self.model.evaluate(self.x,self.y, batch_size=size,verbose=1)
		print(self.MSE[0])
		self.results = self.model.predict(self.x,batch_size=size,verbose=1)

	def get_time(self,i):
		athlete = json.dumps(self.x[i].tolist())
		predicted = json.dumps(self.results[i].tolist())
		expected = json.dumps(self.y[i].tolist())

		dct = {}
		dct['athlete'] = athlete.replace("\"","").decode('unicode_escape').encode('ascii','ignore')
		dct['predicted'] = predicted.strip()
		dct['expected'] = expected.replace("\"","").decode('unicode_escape').encode('ascii','ignore')
		return dct


	def predict_helper(self, results_list, RMSE):

		return '{"values":'+str(json.dumps(results_list))+','+'"RMSE":'+ RMSE+'}'
	def predict(self, x, length):
		x = np.asarray(x)
		temp = length*2
		#temp = length
		x = np.resize(x,(1,1,size))
		
		#print(x)
		#x, x1 = self.split(x)
		for i in range(temp, len(x[0][0])):
			x[0][0][i] = 0
			#x1[0][0][i] = 0
		results = self.model.predict(x,batch_size=size)
		final = results
		i = 2
		month = float(results[0][0][1])
		time = float(results[0][0][0])
		while temp < size/2:
			x[0][0][temp] = results[0][0][0]
			x[0][0][temp+1] = results[0][0][1]
			#x1[0][0][temp] = results[0][0][1]
			
			final[0][0][i] = x[0][0][temp]
			final[0][0][i+1] = x[0][0][temp+1]
			
			temp = temp + 2
			i = i + 2

			results = self.model.predict(x,batch_size=size)
			if  x[0][0][temp+1] > month:
				
				month = float(results[0][0][1])
				time = float(results[0][0][0])
			else:
				
				break;

		results[0][0][1] = month
		results[0][0][0] = time
		#print(x)
		#print(x1)
		print(json.dumps(final.tolist()))
		return final.tolist(), str(math.sqrt(self.MSE[0]))
	# here for merge modes

	def split(self,x):
		tmp1 = list()
		tmp2 = list()
		for i in x:
			sub1 = list()
			sub2 = list()
			for j in range(size):

				if j % 2 == 0:
					sub1.append(i[0][j])
					print j
				else:
					sub2.append(i[0][j])
			tmp1.append([sub1])
			tmp2.append([sub2])
		#print(tmp1)


		return np.asarray(tmp1), np.asarray(tmp2)
	def histogram(self):
		histogram = list()
		scatter = list()
		for i in range(len(self.results)):
			value = round(float(self.results[i][0][0]) - float(self.x[i][0][0]),3)
			scatterval = [value, round(float(self.results[i][0][1]) - float(self.x[i][0][1]),3)]
			if value >= -3 and value <= 3:
				histogram.append(value)
				scatter.append(scatterval)
		return '{"values":'+json.dumps(histogram)+',"scatter":'+json.dumps(scatter)+'}'
