import storyData as sd
import sortByLabel as sbl

TARGET = 'ISCO08_1'

labels, cleanCatData = sd.getCatData()
storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)
# newData = sd.categoryDataMaker(TARGET, labels, storiesData, 100)

sdata, slabels = sbl.splitForStory(TARGET, labels, cleanCatData)
for s in sdata:
    print s.shape
