import numpy as np
import decimal
import sortByLabel as sbl
import generateData as gd
from sklearn.ensemble import IsolationForest as skiso

STORYDATAPATH = 'story/storyData.npy'
LABELPATH = 'full/labelsFull.npy'
CLEANDATAPATH = 'full/cleanDataFull.npy'
CLEANSUBDATAPATH = 'full/cleanDataSub.npy'


DATAFILE = 'full/RBFP-RDrives-CA dataset DEF.csv'
DELIMITER = ';'
# 
# seed = 42
# np.random.seed(seed)
rng = np.random.RandomState()

# clean takes an element, parses it for float castability,
# and returns the correct float value to be inserted
def clean(elem):
		if elem == '' or elem == ' ':
			elem = -1.0
		else:
			try:
				elem = float(elem.replace(",","."))
			except ValueError:
				print "Faulty entry: " + elem
				elem = -1.0
		return elem


# Assumes dataset has 1 row of categories in string format
# create a dataset where empty fields are replaced by -1
# returns labels and data set as numpy array
def getCatData():
	try:
		cleanData = np.load(CLEANDATAPATH)
		labels = np.load(LABELPATH)
	except IOError:
		# print "One or more files not found, generating new..."

		rawData = np.genfromtxt(DATAFILE, dtype=decimal.Decimal, delimiter = DELIMITER)

		labels = rawData[0, :]
		np.save(LABELPATH, labels)

		(dataRows, dataCols) = rawData.shape

		cleanData = np.empty((dataRows-1, dataCols), float)

		for i in range(1, dataRows):
			for j in range(0, dataCols):
				cleanData[i-1,j] = clean(rawData[i,j])

		np.save(CLEANDATAPATH, cleanData)

	return labels, cleanData

# Assumes empty fields have been filled with -1.0
# input label (categories), array of labels, and dataset (numpy array)
# returns an array with a numpy array for each category with a per category
# augmented IQ score where there where non. Sampled from the distribution in
# the category.
def fillStoryIq(label, labels, data):
    catArrays, storyLabels = sbl.splitForStory(label, labels, data)
    # for each targetted category clean and supplement data.
    storyArray = []
    # for non categorical columns use addSample
    for cat in catArrays:
        storyData = cat
        noiq_idx = np.where(cat[:,-1] == -1.)
        # place a sampled value in placeholder (-1) indexes
        hasValues = np.where(cat[:,-1] != -1.)
        mu = cat[:,-1][hasValues].mean()
        sigma = cat[:,-1][hasValues].std()/1.2
        storyData[noiq_idx[0],-1] = np.random.normal(mu, sigma, len(noiq_idx[0]))
        storyArray.append(storyData)
    return np.array(storyArray)


# Assumes an array of for non-categorical columns complete numpy arrays.
# Creates array for each category datapoints amount, with filled in category
# generates data with normal distribution of known points
# returns an array of numpy arrays per category with generated to #datapoints
def categoryDataMaker(label, labels, array, datapoints):
	makerArray = []
	for cat in array:
		if cat.shape[0] < datapoints:
			labelpos = np.where(labels == label)
			labelcat = cat[0,labelpos[0][0]]
			newcat = np.zeros((datapoints, cat.shape[1]))
			newcat.fill(-1)
			newcat[0:cat.shape[0],:] = cat
			newcat[:,labelpos[0][0]] = labelcat
			mus = cat[:,10:].mean(0)
			mus1 = mus[:20]
			mus2 = mus[20:]
			sigmas = cat[:,10:].std(0)
			sigmas1 = sigmas[:20]
			sigmas2 = sigmas[20:]
			for i in range(cat.shape[0], datapoints - cat.shape[0]):
				new1 = np.random.normal(mus1, sigmas1, len(mus1))
				new2 = np.random.normal(mus2, sigmas2, len(mus2))
				newRow = np.concatenate((new1, new2,), 0)
				newcat[i,10:] = newRow
				newcat[i,0] = -2
		else:
			newcat = cat[:datapoints,:]

		makerArray.append(newcat)

	return np.array(makerArray)


def fakeDataMaker(label, labels, array, datapoints):
	makerArray = []
	for cat in array:
		if cat.shape[0]:
			labelpos = np.where(labels == label)
			labelcat = cat[0,labelpos[0][0]]
			newcat = np.zeros((datapoints, cat.shape[1]))
			newcat.fill(-1)
			newcat[:,labelpos[0][0]] = labelcat
			newcat[:,0] = -2
			mus = cat[:,10:].mean(0)
			mus1 = mus[:20]
			mus2 = mus[20:]
			sigmas = cat[:,10:].std(0)
			sigmas1 = sigmas[:20]
			sigmas2 = sigmas[20:]
			for i in range(datapoints):
				new1 = np.random.normal(mus1, sigmas1, len(mus1))
				new2 = np.random.normal(mus2, sigmas2, len(mus2))
				newRow = np.concatenate((new1, new2,), 0)
				newcat[i,10:] = newRow
			makerArray.append(newcat)
		else:
			continue
	return np.array(makerArray)


# data maker per column. finds outliers per column
def inlierDataMaker(label, labels, array, datapoints, strength):
	makerArray = []
	for cat in array:
		labelpos = np.where(labels == label)
		labelcat = cat[0,labelpos[0][0]]
		newcat = np.zeros((datapoints, cat.shape[1]))
		newcat.fill(-1)
		newcat[:,labelpos[0][0]] = labelcat
		newcat[:,0] = -2
		mus = cat[:,11:].mean(0)
		sigmas = cat[:,11:].std(0)
		idxHigh = np.where(cat[:,11:] > mus+strength*sigmas)[0]
		idxLow = np.where(cat[:,11:] < mus-strength*sigmas)[0]
 		deleteIdx = np.union1d(idxHigh, idxLow)
		cleanCat = np.delete(cat, deleteIdx, 0)
		cleanMus = cleanCat[:,11:].mean(0)
		cleanSigmas = cleanCat[:,11:].std(0)
		mus1 = cleanMus[:20]
		mus2 = cleanMus[20:]
		sigmas1 = cleanSigmas[:20]
		sigmas2 = cleanSigmas[20:]
		for i in range(datapoints):
			new1 = np.random.normal(mus1, sigmas1, len(mus1))
			new2 = np.random.normal(mus2, sigmas2, len(mus2))
			newRow = np.concatenate((new1, new2,), 0)
			newcat[i,11:] = newRow
		makerArray.append(newcat)
	return np.array(makerArray)


def standardDataMaker(label, labels, array, datapoints, strength):
	makerArray = []
	for cat in array:
		labelpos = np.where(labels == label)
		labelcat = cat[0,labelpos[0][0]]
		newcat = np.zeros((datapoints, cat.shape[1]))
		newcat.fill(-1)
		newcat[:,labelpos[0][0]] = labelcat
		newcat[:,0] = -2
		colMus = []
		colSigs = []
		for j in range(11, cat.shape[1]):
			colMu = cat[:,j].mean(0)
			colSig = cat[:,j].std(0)
			idxHigh = np.where(cat[:,j:] > colMu+strength*colSig)[0]
			idxLow = np.where(cat[:,j:] < colMu-strength*colSig)[0]
			deleteIdx = np.union1d(idxHigh, idxLow)
			cleanCol = np.delete(cat[:,j], deleteIdx, 0)
			mu = cleanCol.mean(0)
			sigma = cleanCol.std(0)
			colMus.append(mu)
			colSigs.append(sigma)
		for i in range(datapoints):
			mus1 = np.array(colMus)[:20]
			mus2 = np.array(colMus)[20:]
			sigmas1 = colSigs[:20]
			sigmas2 = colSigs[20:]
			new1 = np.random.normal(mus1, sigmas1, len(mus1))
			new2 = np.random.normal(mus2, sigmas2, len(mus2))
			newRow = np.concatenate((new1, new2,), 0)
			newcat[i,11:] = newRow
		makerArray.append(newcat)
	return np.array(makerArray)

def isoDataMaker(catArrays):
	dataSet = []
	for X in catArrays:
		np.random.shuffle(X)
		clf = skiso(n_estimators=20, random_state=rng, n_jobs=-1)
		clf.fit(X)
		predicted = clf.predict(X)
		abnormal = X[predicted == -1]
		normal = X[predicted == 1]
		dataSet.append(normal)
	return np.array(dataSet)




## NEEDS DEBUG
# Inputs: Target, labelset and dataset. Returns array with dimension size of the
# number of categories, with datapoints filled with per column based mean for
# each category.
def fillEmptyWithCategorieColumnDistribution(label, labels, data):
    catArrays, storyLabels = sbl.splitForStory(label, labels, data)
    # for each targetted category clean and supplement data.
    storyArray = []
    # for non categorical columns use addSample
    for cat in catArrays:
        categories = cat[:,0:10]
        testresults = cat[:,10:]
        rows, cols = testresults.shape
        storyData = testresults
        indexes = np.where(testresults == -1)
        # place a sampled value in placeholder (-1) indexes
        for j in indexes[1]:
            ########## MOET EVEN ALLEEN OP INGEVULDE WAARDES WERKEN)
            hasValues = np.where(testresults[:,j] != -1.)
            mu = testresults[hasValues].mean()
            sigma = testresults[hasValues].std()
            storyData[indexes[0],j] = np.random.normal(mu, sigma, len(indexes[0]))
        concat = np.concatenate((categories, storyData),1)
        storyArray.append(concat)
    # build string for concat)
    concat = storyArray[0]
    for story  in range(1, len(storyArray)):
        concat = np.concatenate(concat, storyArray[story],0)
    return np.array(storyArray)

# Expects n dimensional array, with numpy arrays. feature length must be equal
# for all np arrays in array.
# returns numpy array
def construcDataFromArray(array):
    concat = array[0]
    for i in range(1, len(array)):
        concat = np.concatenate((concat, array[i]),0)
    return concat








# [20:30,10:]
