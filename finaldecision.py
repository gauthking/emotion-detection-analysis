import csv
import time
import winsound
from datetime import datetime
list1 = []
list2 = []
flagCount = 0
flagCount1 = 0
flagCount2 = 0

beepFreq = 1500
duration = 1400

while True:
    with open('distressRanges.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (row not in list1 and row != [] and row != ['starttime', 'endtime', 'seconds']):
                list1.append(row)  # or do something with the row data
                flagCount1 += 1

    with open('bpmRanges.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (row not in list2 and row != [] and row != ['starttime', 'endtime', 'seconds']):
                list2.append(row)  # or do something with the row data
                flagCount2 += 1

    try:
        if (list1 != [] and list2 != []):
            # overlap logic
            if (((datetime.strptime(list2[flagCount][0], "%H:%M:%S") > datetime.strptime(list1[flagCount][0], "%H:%M:%S")) and (datetime.strptime(list2[flagCount][0], "%H:%M:%S") < datetime.strptime(list1[flagCount][1], "%H:%M:%S"))) or ((datetime.strptime(list1[flagCount][1], "%H:%M:%S") > datetime.strptime(list2[flagCount][0], "%H:%M:%S")) and (datetime.strptime(list1[flagCount][1], "%H:%M:%S") < datetime.strptime(list2[flagCount][1], "%H:%M:%S")))):
                print("Distress levels and Heart rate high")
                flagCount += 1
                winsound.Beep(beepFreq, duration)

            elif (((datetime.strptime(list1[flagCount][0], "%H:%M:%S") > datetime.strptime(list2[flagCount][0], "%H:%M:%S")) and (datetime.strptime(list1[flagCount][0], "%H:%M:%S") < datetime.strptime(list2[flagCount][1], "%H:%M:%S"))) or ((datetime.strptime(list2[flagCount][1], "%H:%M:%S") > datetime.strptime(list1[flagCount][0], "%H:%M:%S")) and (datetime.strptime(list2[flagCount][1], "%H:%M:%S") < datetime.strptime(list1[flagCount][1], "%H:%M:%S")))):
                print("Distress levels and Heart rate high")
                flagCount += 1
                winsound.Beep(beepFreq, duration)

    except IndexError as e:
        continue

    time.sleep(1)
