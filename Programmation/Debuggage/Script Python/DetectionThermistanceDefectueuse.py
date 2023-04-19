import matplotlib.pyplot as plt
import numpy as np
import os

dataPath = os.path.dirname(os.path.abspath(__file__)) + "/vrai_test_escalier_17_avril.txt"

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

def datas():
	time = importCol(dataPath, 0)

	thermistances = []
	for i in range(6, 70):
		thermistances.append(importCol(dataPath, i))
	mux1 = thermistances[0:16]
	mux2 = thermistances[16:32]
	mux3 = thermistances[32:48]
	mux4 = thermistances[48:64]
	return (time, mux1, mux2, mux3, mux4)


if __name__ == "__main__":
	# arrayAcquisition = [8,19,20,22,3,9,12,18,21,23,2,6,10,13,24,26,25,1,5,7,14,31,27,29,28,0,4,55,11,15,43,30,33,34,62,63,56,51,47,32,35,36,60,61,52,46,42,37,38,59,57,53,45,41,39,58,54,44,40]
	# indice = [39,38,59,58,40,21,20,37,36,57,41,22,9,8,19,35,56,42,23,10,2,7,18,34,55,43,24,11,3,1,6,17,33,54,44,25,12,4,5,16,32,53,45,26,13,14,15,31,52,46,27,28,29,30,51,47,48,49,50]



	# mux1(rouge),mux2(bleu),mux3(vert),mux4(orange)
	indiceMux1 = [43, 42, 41, 40, 24, 23, 22, 10, 39, 21, 9, 3, 20, 8, 2, 1]
	indiceMux2 = [101, 102, 37, 38, 59, 36, 58, 57, 19, 56, 35, 18, 55, 34, 17, 7]
	indiceMux3 = [16, 33, 54, 32, 53, 31, 52, 51, 50, 30, 15, 6, 49, 29, 14, 5]
	indiceMux4 = [103, 104, 105, 4, 13, 28, 48, 11, 12, 27, 47, 46, 45, 26, 44, 25]

	time, mux1, mux2, mux3, mux4 = datas()
	indiceAberant = indicesAberant(indiceMux1, indiceMux2, indiceMux3, indiceMux4, mux1, mux2, mux3, mux4)
	indiceDansMux4 = indiceAberantDansMux4(indiceAberant, indiceMux4)

	fig, ax = plt.subplots(nrows=2, ncols=2)
	for i, x in enumerate(mux1):
		ax[0][0].plot(time, x)
		ax[0][0].plot([time[750],time[750]], [4,2.5])
		ax[0][1].plot(time, mux2[i])
		ax[1][0].plot(time, mux3[i])
		ax[1][1].plot(time, mux4[i])
	plt.show()
