import csv
import pandas as pd
import numpy as np

import sys

sys.path.append('../../')

import sentiment as factory_file
    
validServices = [
    factory_file.CLARIFAI,
    factory_file.MICROSOFT,
    factory_file.IBM,
    factory_file.KOMPREHEND,
    factory_file.LETTRIA,
    factory_file.MEANING_CLOUD,
    factory_file.DANDELION,
    factory_file.MONKEYLEARN,
    factory_file.UCLASSIFY,
    factory_file.GOOGLE
]

tested_data = pd.read_csv('sentiment_processed_data.csv')

count = {}
for row in tested_data[tested_data.columns[1]]:
    if row not in count:
        count[row] = 1
    else:
        count[row] += 1

print(count)


sentiment_vals = []
trueValues = tested_data[tested_data.columns[1]]

for columnCount in range(len(validServices)):
    sentiment_map = {}
    sentiment_map['truepositive'] = 0
    sentiment_map['truenegative'] = 0
    sentiment_map['falsenegative'] = 0
    sentiment_map['falsepositive'] = 0

    for rowCount in range(len(trueValues)):
        if type(tested_data[tested_data.columns[2 + columnCount]][rowCount]) != str:
            continue

        if trueValues[rowCount] == "negative":
            if trueValues[rowCount] == tested_data[tested_data.columns[2 + columnCount]][rowCount]:
                sentiment_map["truenegative"] += 1
            elif tested_data[tested_data.columns[2 + columnCount]][rowCount] == "positive":
                sentiment_map["falsepositive"] += 1
        elif trueValues[rowCount] == "positive":
            if trueValues[rowCount] == tested_data[tested_data.columns[2 + columnCount]][rowCount]:
                sentiment_map["truepositive"] += 1
            elif tested_data[tested_data.columns[2 + columnCount]][rowCount] == "negative":
                sentiment_map["falsenegative"] += 1
        
    sentiment_vals.append(sentiment_map)


temp = []
for row in sentiment_vals:
    a = []
    for key, value in row.items():
        if key == "truenegative" or key == "falsepositive":
            a.append(value / count['negative'])
        else:
            a.append(value / count['positive'])
    temp.append(a)
    print(row)


df = pd.DataFrame(list(zip(*temp))).add_prefix('Col')

df.to_csv('results.csv', index=False)

print(df)

