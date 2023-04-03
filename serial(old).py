import serial
import csv
import datetime
import pandas as pd

fields = ["bpm", "time"]
with open("bpmVtime.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    csv_writer.writeheader()

count = 0

while True:
    ser = serial.Serial('COM10', 9600, timeout=1)
    print(ser.readline())
    with open("bpmVtime.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        info = {
            "bpm": ser.readline(),
            "time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        csv_writer.writerow(info)
    ser.close()
