import numpy as np
import pandas as pd

def discretiseValue(x, m, bin_size):
	if x < (m - bin_size): return(0)
	elif x < m: return(1)
	elif x < (m + bin_size): return(2)
	else: return(0)

def discretiseFeature(feature):
	m = np.mean(feature)
	bin_size = np.std(feature)
	feature = map(lambda x: discretiseValue(x, m, bin_size), np.nditer(feature))
	return(feature)

def discretiseFeatureSet(featureset):
	featureset = np.apply_along_axis(discretiseFeature, 1, featureset)
	return(featureset)

def uniqueDiscreteFeatures(featureset):
	featureset = discretiseFeatureSet(featureset)
	d0 = 3
	for i in range(1,37):
		featureset[:,i] = featureset[:,i]+d0
		d0 += 3
	return(featureset)
