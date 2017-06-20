import numpy as np
import decimal
import sortByLabel as sbl
import generateData as gd

STORYDATAPATH = 'story/storyData.npy'
LABELPATH = 'full/labelsFull.npy'
CLEANDATAPATH = 'full/cleanDataFull.npy'
CLEANSUBDATAPATH = 'full/cleanDataSub.npy'


DATAFILE = 'full/RBFP-RDrives-CA dataset DEF.csv'
DELIMITER = ';'

seed = 21
np.random.seed(seed)


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
#
def categoryDataMaker(label, labels, array, datapoints):
    for cat in array:
        print cat.shape

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
        categories = cat[:,0:11]
        testresults = cat[:,11:]
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








# [20:30,11:]
