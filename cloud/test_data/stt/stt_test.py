import pandas as pd
from pprint import pprint
import csv
import json
import time
import sys
import jiwer
import string
from os.path import join, dirname
import os

# MOCKING
import os
from dotenv import load_dotenv
load_dotenv()
MOCKING_TEST = os.getenv("MOCKING")
MOCKING_VAR = MOCKING_TEST == 'True'

sys.path.append('../../')

import stt as factory_file

# Data folder and type
folderName = "test-clean"
filetype = ".flac"

# VARS
printToCSV = True
# Number of keys to be tested per
wantedDataEntries = 100
# Data that has already been tested (should be wantedDataEntries after a run)
testedData = 0
# 70968 -> 1-63     Male 1 speaker
# 70970 -> 64 - 101           
# 126133 -> 102 - 127               Female 1 Speaker
# 134493 -> 128 - 146
# 134500 -> 147 -> 188
# 123286 -> 189 -> 220              Male 2 speaker
# 123288 -> 221 -> 249
# 123440 -> 250 -> 270
# 1221-135766 and 135767 -> 271 - 311       Female 2
# 672-122797 -> 312 - 379                   Male 3
# Female 3 -> 380 - 442



if MOCKING_VAR:
    printToCSV = False
    
validServices = [
    factory_file.ASSEMBLY_AI,
    factory_file.DEEPGRAM,
    factory_file.GOOGLE,
    factory_file.MICROSOFT,
    factory_file.IBM
]

with open('filesAndResults.csv') as file:
    reader = csv.reader(file)
    tested_data = pd.read_csv('stt_tested_data.csv')
    mocking_stt = pd.read_csv('mocking_stt.csv')


    filteredData = {}
    loadCounter = 0
    tested_data_sentences = [
        value for value in tested_data[tested_data.columns[0]]]

    for row in reader:
        mapIndex = join(folderName, row[0] + filetype)
        if mapIndex not in tested_data_sentences:
            filteredData[mapIndex] = row[1]



with open(join(dirname(dirname(dirname(__file__))), 'keys.json'), 'r') as f:
    keys = json.load(f)


dict_entries = {}
for SERVICE in validServices:
    dict_entries[SERVICE] = {}
    dict_entries[SERVICE]['correctDataEntries'] = 0
    dict_entries[SERVICE]['totalDataEntries'] = 0

j = 0
final = []
mocked_data = []
for key in filteredData:
    if key in tested_data_sentences:
        print("Duplicate")
        continue
    dataList = []
    mockedList = []
    mockedList.append(key)
    mockedList.append(filteredData[key].lower())
    dataList.append(key)
    dataList.append(filteredData[key].lower())

    for SERVICE in validServices:
      
        model = factory_file.STT(SERVICE, keys)
        if (j < wantedDataEntries):
            try:
                response = model(key.strip())

                if response != None:
                    returnValue = response

                    if MOCKING_VAR and returnValue['text'].lower() == "dummy text":
                        dict_entries[SERVICE]['correctDataEntries'] += 1   
                    else:
                        # Get rid of punctuation
                        final_key = returnValue['text'].lower().translate(str.maketrans('', '', string.punctuation))
                        wer = jiwer.wer(filteredData[key].lower(), final_key)

                        if wer < 0.20:
                            dict_entries[SERVICE]['correctDataEntries'] += 1


                        dataList.append(wer)
                        mockedList.append(response)
                else:
                    dataList.append(None)
                    mockedList.append(None)

                dict_entries[SERVICE]['totalDataEntries'] += 1
            
            except:
                print("Something went wrong - ", SERVICE, '\n')
                dataList.append(None)
                continue

    if j >= wantedDataEntries:
        break
    j += 1
    if not(MOCKING_VAR):
        print(j, ": ", dataList)
    final.append(dataList)
    mocked_data.append(mockedList)


for SERVICE in validServices:
    ttlData = dict_entries[SERVICE]['totalDataEntries']
    ttlCorrect = dict_entries[SERVICE]['correctDataEntries']
    if ttlData != 0:
        print(SERVICE, " scored ", ttlCorrect, " out of ", ttlData,
              " entries correct. This is ", 100 * ttlCorrect/ttlData, " percent correct.")
    else:
        print("Something else went wrong, total Data = 0", '\n')


if printToCSV:
    with open('stt_tested_data.csv', 'a', encoding="UTF8", newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        for row in final:
            writer.writerow(row)

        f.close()
    
    # Mocked Data
    with open('mocking_stt.csv', 'a', encoding="UTF8", newline='') as f1:
        # create the csv writer
        writer1 = csv.writer(f1)

        # write a row to the csv file
        for row in mocked_data:
            writer1.writerow(row)

        f1.close()




# os.remove("tempData.json")

