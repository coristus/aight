import discretise
import storyData as sd
import numpy as np
import pandas as pd
from apyori import apriori

def optimSupport(max_profiles, min_dim, min_sup, delta, featureset):
	n_profiles = max_profiles + 1
	min_sup -= delta
	while (n_profiles > max_profiles):
		min_sup += delta
		results = apriori(featureset, min_support=min_sup)
		profiles = map(lambda x: x.items, filter(lambda u: len(u.items) >= min_dim, results))
		n_profiles = len(profiles)
		print '%d profiles found with a minimum support of %.4f' % (n_profiles, min_sup)
	return min_sup

labels, data = sd.getCatData()
# data[:,11:] = discretise.uniqueDiscreteFeatures(data[:,11:])

# sup = optimSupport(10, 4, .129, .0001, data[:,11:])
# print sup

# results = apriori(data[:,11:], min_support=0.1291)
# print pd.DataFrame(map(lambda x: (x.items, x.support), filter(lambda u : len(u.items)>3, results)))
