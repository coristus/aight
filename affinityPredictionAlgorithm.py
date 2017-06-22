from keras.models import load_model
import numpy as np


# input a model choice and a vector of test results
# output an array of percentage per categories (from 0...n) and which algorithm
def getAffinity(vector):
	person = np.array(vector).reshape(1,len(vector))
	model1 = load_model('ISCO08_1_256_256_256.h5')
	chances1 = model1.predict([person])
	model2 = load_model('ISCO08_1_256_256.h5')
	chances2= model2.predict([person])
	model3 = load_model('ISCO08_1_256.h5')
	chances3 = model3.predict([person])
	chances_are = (chances1+chances2+chances3)/3.
	perc = chances_are[0].flatten()*100
	algo = 'Combined Algo'
	return perc, algo
