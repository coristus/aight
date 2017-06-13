import numpy as np
import decimal

def clean(elem):
		if elem == '' or elem == ' ':
			elem = 0.0
		else:
			try:
				elem = float(elem.replace(",","."))
			except ValueError:
				print "Faulty entry: " + elem
				elem = -1.0
		return elem

def getData():
	CLEANDATAPATH = 'full/cleanDataFull.npy'

	try:
		cleanData = np.load(CLEANDATAPATH)
	except IOError:
		print "File not found, generating new..."

		DATAFILE = 'full/RBFP-RDrives-CA dataset DEF.csv'
		DELIMITER = ';'

		rawData = np.genfromtxt(DATAFILE, dtype=decimal.Decimal, delimiter = DELIMITER)

		(dataRows, dataCols) = rawData.shape

		cleanData = np.empty((dataRows-1, dataCols), float)

		for i in range(1, dataRows):
			for j in range(0, dataCols):
				cleanData[i-1,j] = clean(rawData[i,j])

		np.save(CLEANDATAPATH, cleanData)

	return cleanData
