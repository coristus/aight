import storyData as sd
import sortByLabel as sbl
import numpy as np

TARGET = 'ISCO08_1'

labels, cleanCatData = sd.getCatData()
print cleanCatData.shape
targetColumnNr = np.where(labels == TARGET)[0][0]
# fill iq scores for better training
# storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)

catArrays, storyLabels = sbl.splitNoEmptyStory(TARGET, labels, cleanCatData)
print catArrays
# Make balanced dataset
# balancedData = sd.categoryDataMaker(TARGET, labels, storiesData, 1000)
#
# fakeData = sd.fakeDataMaker(TARGET, labels, storiesData, 2500)


bla = sd.construcDataFromArray(catArrays)

print bla.shape

# test = sd.construcDataFromArray(balancedData)

# data = sd.construcDataFromArray(fakeData)
