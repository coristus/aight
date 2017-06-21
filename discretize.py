import numpy as np

def discretizeValue(x, m, bin_size):
	if x < (m - bin_size):
		x = 0
	elif x < m:
		x = 1
	elif x < (m + bin_size):
		x = 2
	else:
		x = 3
	return(x)

def discretizeFeature(feature):
	m = np.mean(feature)
	bin_size = np.std(feature)
	feature = map(lambda x: discretizeValue(x, m, bin_size), np.nditer(feature))
	return(feature)

def discretizeData(data):
	data = np.apply_along_axis(discretizeFeature, 1, data)
	return(data)
