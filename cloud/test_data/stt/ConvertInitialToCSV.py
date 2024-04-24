import csv

filetext = "1284-134647.trans.txt"
with open(filetext, newline='') as input_file:
    lines = input_file.readlines()

    temp = []
    for line in lines:
        line = line[:-1]
        bruh = line.split(" ")
        a = " ".join(bruh[1:])
        b = [bruh[0]]
        b.append(a)
        temp.append(b)

    with open('filesAndResults.csv', 'w', encoding="UTF8", newline='') as f:
        writer = csv.writer(f)

        for value in temp:
            writer.writerow(value)
        
        f.close()
    input_file.close()


