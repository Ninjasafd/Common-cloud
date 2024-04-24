import pandas as pd
import csv
import json
import time
import sys
from os.path import join, dirname

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

sys.path.append('../../')

import sentiment as factory_file

# VARS
printToCSV = True
# Number of keys to be tested per
wantedDataEntries = 100
# Data that has already been tested (should be wantedDataEntries after a run)
testedData = 810   # 810 for positive     # 810 negative

if MOCKING_VAR:
    printToCSV = False

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
validSentiments = ["negative"]
# Sentiments you want to sort out
# positive, negative, neutral

# df = pd.read_csv('sentiment_data.csv')
# data = df.to_json("sentiment_temp.json")

tested_data = pd.read_csv('sentiment_processed_data.csv')

with open("sentiment_temp.json") as input_file:
    allData = json.load(input_file)


# Filters out the sentiments we want to detect, or all if selected
filteredData = {}
loadCounter = 0
tested_data_sentences = [value for value in tested_data[tested_data.columns[0]]]
if len(tested_data_sentences) >= len(allData['Sentiment']):
    print("All entries are tested")
    exit()

for i in range(len(allData['Sentiment'])):
    if allData == "all" or allData["Sentiment"][str(i)] in validSentiments:
        if loadCounter < testedData:
            loadCounter += 1
        else:
            filteredData[allData["Sentence"][str(i)]] = allData["Sentiment"][str(i)]



with open(join(dirname(dirname(dirname(__file__))), 'keys.json'), 'r') as f:
    keys = json.load(f)


# Compares each data entry in the given test set


dict_entries = {}
for SERVICE in validServices:
    dict_entries[SERVICE] = {}
    dict_entries[SERVICE]['correctDataEntries'] = 0
    dict_entries[SERVICE]['totalDataEntries'] = 0
    

j = 0
final = []
for key in filteredData:
    if key in tested_data_sentences:
        print("Duplicate")
        continue
    
    dataList = []
    
    dataList.append(key)
    dataList.append(filteredData[key])
    
    for SERVICE in validServices:
      
        model = factory_file.Sentiment(SERVICE, keys)
        if (j < wantedDataEntries):
            try:
                response = model(key.strip())

                if response != None:
                    returnValue = response
                                        
                    if SERVICE in factory_file.get_score_type():
                        if returnValue['type'].lower() == filteredData[key]:
                            dict_entries[SERVICE]['correctDataEntries'] += 1
                        dataList.append(returnValue['type'].lower())

                    else:
                        if (max(returnValue, key=lambda key: returnValue[key]).lower() == filteredData[key]):
                            dict_entries[SERVICE]['correctDataEntries'] += 1
                        dataList.append(max(returnValue, key=lambda key: returnValue[key]).lower())


                else:
                    dataList.append(None)

                dict_entries[SERVICE]['totalDataEntries'] += 1

            except KeyboardInterrupt:
                # quit
                sys.exit()
            
            except:
                print("Something went wrong - ", SERVICE, '\n')
                dataList.append(None)
                continue
            
            if not(MOCKING_VAR):
                if (SERVICE == factory_file.MEANING_CLOUD):
                    time.sleep(0.5)
                time.sleep(0.1)

    if j >= wantedDataEntries:
        break
    j += 1
    if not(MOCKING_VAR):
        print(j, ": ", dataList)
    final.append(dataList)

print(dict_entries)
for SERVICE in validServices:
    ttlData = dict_entries[SERVICE]['totalDataEntries']
    ttlCorrect = dict_entries[SERVICE]['correctDataEntries']
    if ttlData != 0:
        print(SERVICE, " scored ", ttlCorrect, " out of ", ttlData,
              " entries correct. This is ", 100 * ttlCorrect/ttlData, " percent correct.")
    else:
        print("Something else went wrong, total Data = 0", '\n')


if printToCSV:
    with open('sentiment_processed_data.csv', 'a', encoding="UTF8", newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        for row in final:
            writer.writerow(row)

        f.close()

# os.remove("tempData.json")
