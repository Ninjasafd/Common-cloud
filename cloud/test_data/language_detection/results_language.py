import csv
import pandas as pd
import numpy as np

import sys

sys.path.append('../../')

import language_detector as factory_file

validServices = [
    factory_file.DANDELION,
    factory_file.DETECTLANGUAGE,
    factory_file.HAPPI,
    factory_file.IBM,
    factory_file.INTELLEXER,
    factory_file.MEANING_CLOUD,
    factory_file.MICROSOFT,
    factory_file.MONKEYLEARN,
    factory_file.UCLASSIFY,
    factory_file.GOOGLE,
]

tested_data = pd.read_csv('language_processed_data.csv')

count = {}
for row in tested_data[tested_data.columns[1]]:
    if row not in count:
        count[row] = 1
    else:
        count[row] += 1



language_vals = []
trueValues = tested_data[tested_data.columns[1]]

for columnCount in range(len(validServices)):
    language_map = {}

    for rowCount in range(len(trueValues)):
        # print(type(tested_data[tested_data.columns[1 + columnCount]][rowCount]))
        if columnCount == 4 and rowCount == len(trueValues) - 1:
            language_map['Turkish'] = 0
        if type(tested_data[tested_data.columns[2 + columnCount]][rowCount]) != str:
            continue
        if trueValues[rowCount] not in tested_data[tested_data.columns[2 + columnCount]][rowCount]:
            continue
        elif trueValues[rowCount] not in language_map:
            language_map[trueValues[rowCount]] = 1
        else:
            language_map[trueValues[rowCount]] += 1
    language_vals.append(language_map)



final = []
firstColumn = ["Language"]
for service in validServices:
    firstColumn.append(service)
final.append(firstColumn)

temp = []
for row in language_vals:
    a = []
    for key, value in row.items():
        a.append(value / count[key])
    temp.append(a)
    print(row)


df = pd.DataFrame(list(zip(*temp))).add_prefix('Col')

df.to_csv('results.csv', index=False)

print("True ", count)   
for i in range(len(language_vals)):
    print(validServices[i], ':', language_vals[i])

print(df)









with open('finalValues.csv', 'w', encoding="UTF8", newline='') as f:
    writer = csv.writer(f)

    for value in final:
        writer.writerow(value)
    
    f.close()



