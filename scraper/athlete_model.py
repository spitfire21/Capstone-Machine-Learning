import keras
import numpy as np
import pandas as pd
from random import shuffle
import matplotlib.pyplot as plt
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,TimeDistributed, LSTM, Activation,GRU, Masking, Embedding, Dropout
from keras.utils.visualize_util import plot

from sklearn.preprocessing import MinMaxScaler
enc = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
day_of_month = [0,31,29,31,30,31,30,31,31,30,31,30,31]
sizeofinput = 32
size = 128
def convert_date(date):
	res = date.split('/')
	m = res[0]
	m = one_hot(m)
	day = res[1]
	dec = float(float(day)/float(day_of_month[m]))
	
	#if dec > 0.0 and dec < 0.26:
	#	month_decimal = float(m) + 0.0
	#elif dec > 0.25 and dec < 0.51:
#		month_decimal = float(m) + 0.25
#	elif dec > 0.5 and dec < 0.76:
#		month_decimal = float(m) + 0.50
#	else:
#		month_decimal = float(m) + 0.75
	
	return float(m) + round(dec,2)
def load_data(data, labels):
	
	input_listy = list()
	input_listx1 = list()
	
	train_listy = list()
	train_listx1 = list()
	test_len = int(len(data) * 0.25)
	input_len =  int(len(data) * 0.75)
	for i in range(0, input_len - 1):
		listx = list()
		for j in range(0,len(data[i])):
			
			tup1 = (data[i][j], labels[i][j])
			listx.append(tup1)
		tup2 = (data[i][len(data[i]) - 1], labels[i][len(data[i]) - 1])
		input_listy.append(tup2)
		input_listx1.append(listx)
		
		
	for i in range(input_len, len(data)):
		listx = list()
		for j in range(0,len(data[i]) - 1):
			tup1 = (data[i][j], labels[i][j])
			listx.append(tup1)
		tup2 = (data[i][len(data[i]) - 1], labels[i][len(data[i]) - 1])
		train_listy.append(tup2)
		train_listx1.append(listx)
	
	return input_listx1, input_listy, train_listx1, train_listy, test_len, input_len
	
def read_data(data, labels):
	label_lines = list()
	data_lines = list()
	
	with open(data) as f:
		temp = f.readlines()
		
	for i in range (0,len(temp)):
		x = list()
		temp2 = temp[i].split(",")
		for j in temp2:
			x.append(j.strip())
		data_lines.append(x)
		
	with open(labels) as f1:
		temp = f1.readlines()
		
	
	for i in range (0,len(temp)):
		y = list()
		temp2 = temp[i].split(",")
		for j in temp2:
			
			y.append(convert_date(j))
		label_lines.append(y)
	#print(data_lines)
	list1_shuf = []
	list2_shuf = []
	index_shuf = range(len(data_lines))
	shuffle(index_shuf)
	for i in index_shuf:
		list1_shuf.append(data_lines[i])
		list2_shuf.append(label_lines[i])
	return list1_shuf, list2_shuf
	
def one_hot(value):
	return enc[value]
data, labels = read_data('data.txt','labels.txt')
		
lix, liy, tix, tiy, test_len, input_length = load_data(data, labels)



# normalize the dataset
#scaler = MinMaxScaler(feature_range=(0, 1))
#datasetx = scaler.fit_transform(lix)
#datasety = scaler.fit_transform(liy)
#trainsetx = scaler.fit_transform(tix)
#trainsety = scaler.fit_transform(tiy)





datax = list()
datay = list()
for _ in range(len(lix)):
	
	tempx = []
	
	tempy = []
	
	## Something doesnt work with loading data so this is a temp fix
	for i in range(len(lix[_])):
		tempx.append((lix[_][i][0],lix[_][i][1]))
		
			
	
	
	tempy.append((liy[_][0],liy[_][1]))
	###
	
	
	for i in range(len(tempx)):
		while len(tempx) < size/2:
			tempx.append(("0","0"))
			
	for i in range(len(tempy)):
		while len(tempy) < size/2:
			tempy.append(("0","0"))
	tmp = np.asarray(tempx)
	
	#tmp = np.reshape(tmp, (len(tmp),2,1))
	datax.append(tempx)
	datay.append(tempy)
	
	#datax = pd.DataFrame(datax)
	#datay = pd.DataFrame(datay)
	
	#datasety = sequence.pad_sequences(datasety, dtype="float32", maxlen=15)
	
	
	
	

	#X = datasetx[_]
	#Y = datasety[_]




trainx = list()
trainy = list()
for _ in range(len(tix)):
	
	tempx = []
	
	tempy = []
	
	## Something doesnt work with loading data so this is a temp fix
	for i in range(len(tix[_])):
		tempx.append((tix[_][i][0],tix[_][i][1]))
	
	tempy.append((tiy[_][0],tiy[_][1]))
	###
	
	
	for i in range(len(tempx)):
		while len(tempx) < size/2:
			tempx.append(("0","0"))
			
	for i in range(len(tempy)):
		while len(tempy) < size/2:
			tempy.append(("0","0"))
	tmp = np.asarray(tempx)
	
	#tmp = np.reshape(tmp, (len(tmp),2,1))
	trainx.append(tempx)
	trainy.append(tempy)
	
	#datax = pd.DataFrame(datax)
	#datay = pd.DataFrame(datay)
	
	#datasety = sequence.pad_sequences(datasety, dtype="float32", maxlen=15)
	
	
	
	

	#X = datasetx[_]
	#Y = datasety[_]


model = Sequential()  

#model.add(Embedding(19501,2, input_length=15, mask_zero=True))
model.add(Masking(mask_value=0, input_shape=(1,size)))
model.add(LSTM(128, input_length = 1, input_dim = size, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(128, input_length = 1, input_dim = size, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(128, input_length = 1, input_dim = size, return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(128, input_length = 1, input_dim = size, return_sequences=True))
model.add(Dropout(0.5))
model.add(TimeDistributed(Dense(size, input_dim=1)))
model.add(Activation("relu"))  

model.summary()
model.compile(loss="mean_squared_error", optimizer="rmsprop", metrics=['accuracy'])


datax = np.asarray(datax)

datax = np.resize(datax, (input_length,1,size))


datay = np.asarray(datay)

datay = np.resize(datay, (input_length,1,size))


trainx = np.asarray(trainx)
print(trainx[1])
trainx = np.resize(trainx, (test_len,1,size))
print(trainx[1])

trainy = np.asarray(trainy)

trainy = np.resize(trainy, (test_len,1,size))
np.save(open('athletearray.tx','w'),trainx)
np.save(open('athleteresults.tx','w'),trainy)
score = model.fit(datax, datay, batch_size=size, validation_data=(trainx,trainy),nb_epoch=75, shuffle=False)

model.save('100Mmodel.h5')



