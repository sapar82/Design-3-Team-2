from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

dataPath = os.path.dirname(os.path.abspath(__file__)) + "/vrai_test_escalier_17_avril.txt"

def curvefit(x, y, function, P0=False):
	x = np.array(x)
	y = np.array(y)
	if not P0:
		popt, pcov = curve_fit(function, x, y)
	else:
		popt, pcov = curve_fit(function, x, y, p0=P0)
	if len(x) < 1000:
		nbPoint = 1000
	else:
		nbPoint = len(x)
	newDataX = np.linspace(x[0], x[-1], nbPoint)
	newDataY = function(newDataX, *popt)
	newData = {"x": newDataX, "y": newDataY}
	perr = np.sqrt(np.diag(pcov))
	deltaValues = []
	for i in range(len(perr)):
		deltaValues.append(perr[i])
	print("Optimal Parameters: ",popt)
	print("Variance :", deltaValues)
	return popt

def importData(path, splitSymbol, deleteFirstRow=0, xValuesPos=0, yValuesPos=1, normaliseX=False, normaliseY=False):
	fich = open(path, "r")
	fich_str = list(fich)[deleteFirstRow:]
	fich.close()
	x = []
	y = []
	for i in fich_str:
		elem_str = i.replace("\n", "")
		elem_str = i.replace(",", ".")
		elem = elem_str.split(splitSymbol)
		x.append(float(elem[xValuesPos]))
		y.append(float(elem[yValuesPos]))
	if normaliseX == True:
		x = np.array(x)
		x = x - min(x)
		x = x/max(x)
	if normaliseY == True:
		y = np.array(y)
		y = y - min(y)
		y = y/max(y)
	return {"x": x, "y": y}

def importCol(path, xPos, splitSymbol="\t", deleteFirstRow=1):
	fich = open(path, "r")
	fich_str = list(fich)[deleteFirstRow:]
	fich.close()
	x = []
	for i in fich_str:
		elem_str = i.replace("\n", "")
		elem_str = i.replace(",", ".")
		elem = elem_str.split(splitSymbol)
		x.append(float(elem[xPos]))
	return np.array(x)

def indicesAberant(indiceMux1, indiceMux2, indiceMux3, indiceMux4, mux1, mux2, mux3, mux4):
	indiceTot = indiceMux1 + indiceMux2 + indiceMux3 + indiceMux4
	tot = mux1 + mux2 + mux3 + mux4
	count = 0
	indiceAberant = []
	for i, x in enumerate(tot):
		if x[0] > 4.5:
			indiceAberant.append((indiceTot[i]))
			count += 1
	return indiceAberant

def indiceAberantDansMux4(indiceAberant, indiceMux4):
	indiceDansMux4 = []
	count = 0
	for i in indiceAberant:
		if i in indiceMux4:
			indiceDansMux4.append(i)
			count += 1
	return indiceDansMux4

def datas(dataPath):
	time = importCol(dataPath, 0)

	thermistances = []
	for i in range(6, 70):
		thermistances.append(importCol(dataPath, i))
	mux1 = thermistances[0:16]
	mux2 = thermistances[16:32]
	mux3 = thermistances[32:48]
	mux4 = thermistances[48:64]
	return (time, mux1, mux2, mux3, mux4)


def VtoR(v):
	return -1800*v/(v-5)

def VtoT(v):
	r = VtoR(v)
	return -29.03*np.log(r) + 290.3

def degree3(x,a,b,c,d):
	return a*(x**3) + b*(x**2) + c*x + d

def derivative(x, delta = 5):
    """ 
    Return dx/dy
    x : array of values
    return : array of derivative values
    """
    x = np.array(x)
    return (x[delta:] - x[:-delta])

def predictive_algo(x, c, d, delta, separation= False):
	""" 
	Return x ,c * dy/dx , d * d2x/dy2
	x : array of values
	c : array of coefficients
	d : delta of coefficients
	return : array of predicted values
	"""
	x = np.array(x)

	if separation:
	    return x[5:-5], c * derivative(x, delta[0])[5:], d * derivative(derivative(x, delta[1]), delta[2])
	else:
		return x[5:-5]+ c * derivative(x, delta[0])[5:]+ d * derivative(derivative(x, delta[1]), delta[2])

def load_data(datapath):
	"""
	Load the data from the text file and return a dataframe
	"""
	columns = ["time", "power", "x", "y", "tension", 'temp']

	indiceMux1 = [43, 42, 41, 40, 24, 23, 22, 10, 39, 21, 9, 3, 20, 8, 2, 1]
	indiceMux2 = [101, 102, 37, 38, 59, 36, 58, 57, 19, 56, 35, 18, 55, 34, 17, 7]
	indiceMux3 = [16, 33, 54, 32, 53, 31, 52, 51, 50, 30, 15, 6, 49, 29, 14, 5]
	indiceMux4 = ["ref1", "ref2", "ref3", 4, 13, 28, 48, 11, 12, 27, 47, 46, 45, 26, 44, 25]
	#stack all the indices in one array
	datacolumns = np.concatenate((columns, indiceMux1, indiceMux2, indiceMux3, indiceMux4), dtype=str)
	data = pd.read_csv(datapath, sep="\t", skiprows=1)
	data.columns = datacolumns
	data = data.replace(',','.', regex=True)
	data = data.astype(float)
	return data

def rank_temperature(data_temp):
    """
    Return the index of the sensor with the highest temperature
    to the lowest temperature in a list mid way through the data
    """
    data_temp = data_temp.drop(['time', 'power', 'x', 'y', 'tension', 'temp'], axis=1).copy()
    data_temp = data_temp.iloc[len(data_temp)//2]
    data_temp = data_temp.sort_values(ascending=False)
    return data_temp.index

def convert_to_temp(data):
    """
    Create a new dataframe with the temperature in Celsius
    """
    data_temp = data.copy()
    for i in range(1, 59):
        if str(i) in data_temp.columns:
            data_temp[str(i)] = VtoT(data[str(i)])
    return data_temp

if __name__ == "__main__":
	# arrayAcquisition = [8,19,20,22,3,9,12,18,21,23,2,6,10,13,24,26,25,1,5,7,14,31,27,29,28,0,4,55,11,15,43,30,33,34,62,63,56,51,47,32,35,36,60,61,52,46,42,37,38,59,57,53,45,41,39,58,54,44,40]
	# indice = [39,38,59,58,40,21,20,37,36,57,41,22,9,8,19,35,56,42,23,10,2,7,18,34,55,43,24,11,3,1,6,17,33,54,44,25,12,4,5,16,32,53,45,26,13,14,15,31,52,46,27,28,29,30,51,47,48,49,50]



	# mux1(rouge),mux2(bleu),mux3(vert),mux4(orange)
	indiceMux1 = [43, 42, 41, 40, 24, 23, 22, 10, 39, 21, 9, 3, 20, 8, 2, 1]
	indiceMux2 = [101, 102, 37, 38, 59, 36, 58, 57, 19, 56, 35, 18, 55, 34, 17, 7]
	indiceMux3 = [16, 33, 54, 32, 53, 31, 52, 51, 50, 30, 15, 6, 49, 29, 14, 5]
	indiceMux4 = [103, 104, 105, 4, 13, 28, 48, 11, 12, 27, 47, 46, 45, 26, 44, 25]

	time, mux1, mux2, mux3, mux4 = datas(dataPath)
	indiceAberant = indicesAberant(indiceMux1, indiceMux2, indiceMux3, indiceMux4, mux1, mux2, mux3, mux4)
	indiceDansMux4 = indiceAberantDansMux4(indiceAberant, indiceMux4)

	reference = mux2[1]
	data = VtoT(mux1[11])-VtoT(reference)
	y1 = [0, 2.5,5,7.5,10]
	x = [data[0], data[280], data[440], data[600], data[780]]
	x =	np.array(x)

	popt = curvefit(x, y1, degree3)

	fig, ax = plt.subplots(nrows=1, ncols=1)
	# ax.plot(time, data)
	ax.plot(x, y1)
	# ax.plot([data[0],data[780]],[0,10])
	ax.plot(x, degree3(x, *popt))
	ax.grid()
	# n = 1500
	# ax.plot(time, abs(mux1[11]-reference))
	# ax.plot([time[n],time[n]], [0,1.75])
	plt.show()
	
	data = abs(mux1[11]-reference)
	print(data[780])
	nan = "nan"

	indice = [(0,1500),(280,1270),(440,1100),(600,960),780]
	x = [0, 2.5,5,7.5,10]
	y = [(mux1[11][0], mux1[11][1500]), (mux1[11][280], mux1[11][1270]), (mux1[11][440], mux1[11][1100]),(mux1[11][600], mux1[11][960]), 1.505]
	y1 = [data[0], data[280], data[440], data[600], data[780]]