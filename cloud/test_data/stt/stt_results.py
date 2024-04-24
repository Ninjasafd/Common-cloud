import csv
import pandas as pd
import numpy as np

import sys

sys.path.append('../../')

import stt as factory_file
    
validServices = [
    factory_file.ASSEMBLY_AI,
    factory_file.DEEPGRAM,
    factory_file.GOOGLE,
    factory_file.MICROSOFT,
    factory_file.IBM
]

tested_data = pd.read_csv('stt_tested_data.csv')

sizes = [99, 87, 82, 41, 68, 63]

final = []
for i in range(len(validServices)):
    totalcount = 0
    service_final = [0, 0, 0, 0, 0, 0]
    for j in range(len(sizes)):
        count = 0
        while count < sizes[j]:
            count += 1
            totalcount += 1
            # if (tested_data[tested_data.columns[2 + i]][totalcount] != np.float64):
            #     continue
            # print(type(tested_data[tested_data.columns[2 + i]][totalcount]))
            service_final[j] += tested_data[tested_data.columns[2 + i]][totalcount]
    service_final = [x / sizes[j] for x in service_final]
    final.append(service_final)


df = pd.DataFrame(list(zip(*final))).add_prefix('Col')

df.to_csv('stt_final_results.csv', index=False)











# with open('finalValues.csv', 'w', encoding="UTF8", newline='') as f:
#     writer = csv.writer(f)

#     for value in final:
#         writer.writerow(value)
    
#     f.close()



