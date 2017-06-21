from keras.models import load_model
import numpy as np


# input a model choice and a vector of test results
# output an array of percentage per categories (from 0...n) and which algorithm
def getAffinity(model, vector):
	person = np.array(vector).reshape(1,len(vector))
	if model == 1:
		model = load_model('ISCO08_1_256_256_256.h5')
		algo = 'Three Layers'
		chances_are = model.predict([person]])
	if model == 2:
		model = load_model('ISCO08_1_256_256.h5')
		algo = 'Two Layers'
		chances_are = model.predict([person]])
	if model == 3:
		model = load_model('ISCO08_1_256.h5')
		algo = 'One Layer'
		chances_are = model.predict([person]])
	perc = chances_are[0].flatten()*100
	return perc, algo
