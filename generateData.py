import numpy as np
import decimal

CLEANDATAPATH = 'full/cleanDataFull.npy'
CLEANSUBDATAPATH = 'full/cleanDataSub.npy'
LABELPATH = 'full/labelsFull.npy'

DATAFILE = 'full/RBFP-RDrives-CA dataset DEF.csv'
DELIMITER = ';'

##
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

##
# Assumes fixed point decimal entries
# getData tries to load data from meory, if this fails it
# reparses the raw file and cleans it up.
# return - list: labels, array: cleanData
def getData():
	try:
		cleanData = np.load(CLEANDATAPATH)
		labels = np.load(LABELPATH)
	except IOError:
		# print "One or more files not found, generating new..."

		rawData = np.genfromtxt(DATAFILE, dtype=decimal.Decimal, delimiter = DELIMITER)

		if sub:
			rawData = rawData[1:,11:-1]

		labels = rawData[0, :]
		np.save(LABELPATH, labels)

		(dataRows, dataCols) = rawData.shape

		cleanData = np.empty((dataRows-1, dataCols), float)

		for i in range(1, dataRows):
			for j in range(0, dataCols):
				cleanData[i-1,j] = clean(rawData[i,j])

		np.save(CLEANDATAPATH, cleanData)

	return labels, cleanData

##
# same algorithm as getData, but only returns the subset of data
# containing the drives and personality scores, saves data in
# file CLEANSUBDATAPATH path
def getSubData():
	try:
		cleanData = np.load(CLEANSUBDATAPATH)
	except IOError:
		# print "One or more files not found, generating new..."

		rawData = np.genfromtxt(DATAFILE, dtype=decimal.Decimal, delimiter = DELIMITER)
		rawData = rawData[1:,11:-1]

		(dataRows, dataCols) = rawData.shape

		cleanData = np.empty((dataRows-1, dataCols), float)

		for i in range(1, dataRows):
			for j in range(0, dataCols):
				cleanData[i-1,j] = clean(rawData[i,j])

		np.save(CLEANSUBDATAPATH, cleanData)

	return cleanData