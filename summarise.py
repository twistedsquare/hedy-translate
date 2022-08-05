#! /usr/local/bin/python3
# Pre-requisite: Python 3

import collections
import csv

with open('translations.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # First column is canonical, then triples of (manual, forward, backward)
    for row in reader:
        rowValuesAsList = list(row.values())
        canon = rowValuesAsList[0]
        countManualEqAuto = 0
        backwards = []
        for i in range(1, len(rowValuesAsList), 3):
            if rowValuesAsList[i+1].strip() and rowValuesAsList[i+2].strip():
                if rowValuesAsList[i].casefold() == rowValuesAsList[i+1].casefold():
                    countManualEqAuto = countManualEqAuto + 1
                backwards.append(rowValuesAsList[i+2].casefold())
        print(canon + " matched: " + str(countManualEqAuto) + "/" + str(len(backwards)) + " " + str(collections.Counter(backwards)))
