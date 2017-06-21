import csv
import sys

import pandas as pd

class DataService:
    def getAll(self):
        return

    def getFiltered(self, key, val):
        return

    def getObject(self, id):
        return

    def getColumns(self, columns):
        return


class CSVDataService(DataService):
    def __init__(self, csvfileloc, keycolumn="id"):
        self.data = []
        self._keycolumn = keycolumn
        self.dataByID = {}
        with open(csvfileloc) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append(row)
                self.dataByID[row[self._keycolumn]] = row

    def getAll(self):
        return self.data

    def getFiltered(self, key, value):
        filteredData = [d for d in self.data if key in d and d[key] == value]
        return filteredData

    def getObject(self, id):
        if id in self.dataByID:
            return self.dataByID[id]

class PandasDataService(DataService):
    ## Colums contains a list of column names filtering the columns
    ## Passing None to columns means using all columns
    def __init__(self, csv_file_location, delimiter_char = ';', columns=None):
        self.configuration={'dataLocation': csv_file_location}
        self.data = pd.read_csv(csv_file_location, sep=delimiter_char, header=0)
        if columns is not None:
            self.data = self.data.filter(items=columns)

    def getAll(self):
        return self.data

    def getFiltered(self, key, val):
        return self.data.loc[self.data[key] == val]

    def getObject(self, id):
        return

    def getColumns(self, columns):
        return self.data[self.data.columns[columns]]
