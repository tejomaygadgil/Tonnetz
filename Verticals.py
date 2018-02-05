from numpy import mean

def seq(minV, maxV, length): 
	return [int(minV + (maxV - minV) / (length - 1) * i) for i in range(length)]

def Verticals(arr, ind):
	def getMin(im, i):
		imV = [v[i] for v in im]
		values = [mean(v) for v in imV]
		return values.index(min(values))
	return [getMin(arr, i) for i in ind]
