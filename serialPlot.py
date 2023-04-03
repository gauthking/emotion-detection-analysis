import serial
import time
import csv
import datetime

fields = ["bpm", "time"]
with open("bpmVtime.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    csv_writer.writeheader()

ser = serial.Serial('COM10', 9600)

count = 0
while True:
    line = ser.readline()   # read a byte string
    # print(line)
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        string = string.strip()
        num = int(string)  # convert the unicode string to an int
        print(num)
        with open("bpmVtime.csv", 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
            info = {
                "bpm": num,
                "time": datetime.datetime.now().strftime("%H:%M:%S")
            }
            csv_writer.writerow(info)


ser.close()
