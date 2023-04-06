import csv
import time

list1 = []

while True:
    with open('distressRanges.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (row not in list1):
                list1.append(row)  # or do something with the row data
                print(row)

    time.sleep(1)  # check for updates every 1 second
