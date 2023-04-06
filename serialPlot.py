import serial
import time
import csv
from datetime import datetime


fields = ["bpm", "time"]
with open("bpmVtime.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    csv_writer.writeheader()

fields1 = ["bpmFreq", "time"]
with open("bpmFreqVtime.csv", 'w') as csv_file1:
    csv_writer1 = csv.DictWriter(csv_file1, fieldnames=fields1)
    csv_writer1.writeheader()

fields2 = ["starttime", "endtime", "seconds"]
with open("bpmRanges.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields2)
    csv_writer.writeheader()


ser = serial.Serial('COM5', 9600)

start = ''
rangeCount = 0
bpmRange = []
timeRange = []


def detect_alertness(num, time):
    global start
    j = 0
    levels = 0
    for i in range(len(bpmRange)):
        if (num[i] > 75):
            if j == 0:
                start = time[i]
            j += 1
        elif (num[i] < 75 and start != ''):
            levels += 1
            print(
                f"High heart rate level - {levels} start time - {start} end time - {str(time[i])}. Estimated duration - ", datetime.strptime(str(time[i]), "%H:%M:%S") - datetime.strptime(start, "%H:%M:%S"))
            est = datetime.strptime(
                str(time[i]), "%H:%M:%S") - datetime.strptime(start, "%H:%M:%S")
            with open("bpmRanges.csv", 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fields2)
                info = {
                    "starttime": start,
                    "endtime": str(time[i]),
                    "seconds": est
                }
                csv_writer.writerow(info)
            j = 0
            start = ''


def compute_bpm_freq_range(num, ti):
    global bpmRange, timeRange, rangeCount
    temp = {"high": 0, "fine": 0}
    for i in range(len(num)):
        if (num[i] > 95):
            temp["high"] += 1
        else:
            temp["fine"] += 1
    with open("bpmFreqVtime.csv", 'a') as csv_file1:
        csv_writer1 = csv.DictWriter(csv_file1, fieldnames=fields1)
        info = {
            "bpmFreq": (temp["high"]/5)*100,
            "time": ti[0]
        }
        csv_writer1.writerow(info)
    bpmRange.append((temp["high"]/5)*100)
    timeRange.append(ti[0])


count = 0
bpm = []
time = []

while True:
    line = ser.readline()   # read a byte string
    # print(line)
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        string = string.strip()
        num = int(string)  # convert the unicode string to an int
        ti = datetime.now().strftime("%H:%M:%S")
        print(num)
        with open("bpmVtime.csv", 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
            info = {
                "bpm": num,
                "time": ti
            }
            csv_writer.writerow(info)
        count += 1
        bpm.append(num)
        time.append(ti)
    if (count == 5):
        compute_bpm_freq_range(bpm, time)
        count = 0
        bpm = []
        time = []
        rangeCount += 1
    if (rangeCount == 4):
        detect_alertness(bpmRange, timeRange)
        bpmRange = []
        timeRange = []
        rangeCount = 0

ser.close()
