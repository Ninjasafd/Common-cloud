import pandas as pd
from pprint import pprint
import csv
import json
import time
import sys
from os.path import join, dirname
import os

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

sys.path.append('../../')

import language_detector as factory_file

# VARS
printToCSV = True
# Number of keys to be tested per
wantedDataEntries = 29
# Data that has already been tested (should be wantedDataEntries after a run)
testedData = 0    # 750 for English      # 500 for Spanish        # 500   French
    # German: 1903 -> 2367 = 465
    # Portuguese: 2368 -> 2917 = 550
    # Swedish 2918 -> 3417
    # Dutch 3418 -> 3917
    # Russian 3918 -> 4417
    # Danish 4418 -> 4841 = 424
    # Turkish 4842 -> 5312                  -> Intellexer doesn't support


if MOCKING_VAR:
    printToCSV = False
    
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
validLanguages = ["Turkish"]
# This is the list of valid testing languages in the testing data:
# If you want all the languages, select all by uncommenting the following line
# validLanguages = "all"

# Processing a file and converting it a json for simplicity

# df = pd.read_csv('Language_Detection.csv')
# data = df.to_json("tempData.json")

tested_data = pd.read_csv('language_processed_data.csv')

with open("tempData.json") as input_file:
    allData = json.load(input_file)


# Checks if we've reached the end of the dataset and if we're testing duplicate values
filteredData = {}
loadCounter = 0
tested_data_sentences = [
    value for value in tested_data[tested_data.columns[0]]]

if len(tested_data_sentences) >= len(allData['Language']):
    print("All entries are tested")
    exit()

# Filters out the languages we want to detect, or all if selected
for i in range(len(allData['Language'])):
    if allData == "all" or allData["Language"][str(i)] in validLanguages:
        if loadCounter < testedData:
            loadCounter += 1
        else:
            if allData["Language"][str(i)] == "Portugeese":
                filteredData[allData["Text"][str(i)]] = "Portuguese"
            elif allData["Language"][str(i)] == "Sweedish":
                filteredData[allData["Text"][str(i)]] = "Swedish"
            else:
                filteredData[allData["Text"][str(i)]] = allData["Language"][str(i)]

# Open the keys file in the `cloud` folder
with open(join(dirname(dirname(dirname(__file__))), 'keys.json'), 'r') as f:
    keys = json.load(f)


# Initializes the necessary datapoints
dict_entries = {}
for SERVICE in validServices:
    dict_entries[SERVICE] = {}
    dict_entries[SERVICE]['correctDataEntries'] = 0
    dict_entries[SERVICE]['totalDataEntries'] = 0

j = 0
final = []
mocked_data = []
for key in filteredData:
    # Checks for already tested data
    if key in tested_data_sentences:
        print("Duplicate")
        continue
    dataList = []
    mockedList = []
    dataList.append(key)
    dataList.append(filteredData[key])
    mockedList.append(key)
    mockedList.append(filteredData[key])

    for SERVICE in validServices:

        ### This uses the factory class to pull the correct model
        model = factory_file.Language(SERVICE, keys)

        with open(join('..','..', '_' + SERVICE, 'language_map.json')) as f:
            language_conversions = json.load(f)

        if (j < wantedDataEntries):
            if len(key) > 200 and SERVICE == factory_file.HAPPI and not(MOCKING_VAR):
                dataList.append(None)
            else:
                try:
                    ### This uses the factory class model to return a response
                    response = model(key)

                    if response != None:
                        returnedLang = response['language']

                        if MOCKING_VAR:
                            dataList.append(returnedLang)
                            if (filteredData[key] in returnedLang):
                                dict_entries[SERVICE]['correctDataEntries'] += 1

                        # Happi weird cases for Happi Scotts comes before English
                        elif SERVICE == factory_file.HAPPI and not(MOCKING_VAR) and (language_conversions['eng'] == filteredData[key] or
                                                                              (returnedLang == 'sco' and filteredData[key] == "English")):
                            dataList.append(language_conversions[returnedLang])
                            dict_entries[SERVICE]['correctDataEntries'] += 1
                            # Entry is omitted because it can't be tested

                        elif "No_abbreviations" in language_conversions:
                            dataList.append(returnedLang)
                            if (filteredData[key] in returnedLang):
                                dict_entries[SERVICE]['correctDataEntries'] += 1

                        
                        elif returnedLang in language_conversions:
                            dataList.append(language_conversions[returnedLang])
                            if (filteredData[key] in language_conversions[returnedLang]):
                                dict_entries[SERVICE]['correctDataEntries'] += 1
                        
                        mockedList.append(response)
                    else:
                        dataList.append(None)
                        mockedList.append(None)
               

                    dict_entries[SERVICE]['totalDataEntries'] += 1

                except KeyboardInterrupt:
                    # quit
                    sys.exit()
                

                except:
                    print("Something went wrong - ", SERVICE, '\n')
                    dataList.append(None)
                    mockedList.append(None)
                    continue

                if (not(MOCKING_VAR)):
                    if (SERVICE == factory_file.MEANING_CLOUD):
                        time.sleep(0.3)
                    time.sleep(0.1)

            
    if j >= wantedDataEntries:
        break
    j += 1
    if not(MOCKING_VAR):
        print(j, ": ", dataList)

    final.append(dataList)
    mocked_data.append(mockedList)

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
    with open('language_processed_data.csv', 'a', encoding="UTF8", newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        for row in final:
            writer.writerow(row)

        f.close()

    with open('mocking_language.csv', 'a', encoding="UTF8", newline='') as f1:
        # create the csv writer
        writer1 = csv.writer(f1)

        # write a row to the csv file
        for row in mocked_data:
            writer1.writerow(row)

        f1.close()




# os.remove("tempData.json")
