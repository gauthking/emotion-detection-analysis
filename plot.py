import csv
from matplotlib import pyplot as plt
import time
from scipy import signal, fft, interpolate
from datetime import datetime
import pandas as pd


windowSize1 = 10
windowSize2 = 50

count = 0

# print(emotionsMain)

start = ''


def compute_threshold_ranges(window1Frequency, timeMain):
    global start
    print(timeMain[0])
    j = 0
    levelsCount = 0
    for i in range(len(window1Frequency)):
        if (window1Frequency[i] > 75):
            if j == 0:
                start = timeMain[i]
                print(start)
            j += 1
        elif (window1Frequency[i] < 75 and start != ''):
            levelsCount += 1
            print(
                f"Distraction level - {levelsCount} start time - {start} end time - {str(timeMain[i])}. Estimated duration of distraction - ", datetime.strptime(str(timeMain[i]), "%H:%M:%S") - datetime.strptime(start, "%H:%M:%S"))
            j = 0
            start = ''
       


fields = ["DistressFreq", "Time"]
with open("freqvtimew1.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
    csv_writer.writeheader()

time.sleep(10)
window1Frequency = []
window1Time = []
for ch in pd.read_csv("plot3.csv", chunksize=windowSize1):
    timeMain = list(ch['Time'])
    tempDict = {"tD": 0, "tN": 0}
    for i in ch['Mood']:
        if (i == "Distracted"):
            tempDict['tD'] += 1
        else:
            tempDict['tN'] += 1
    window1Frequency.append((tempDict['tD']/windowSize1)*100)
    window1Time.append(timeMain[0])
    with open("freqvtimew1.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        info = {
            "DistressFreq": (tempDict['tD']/windowSize1)*100,
            "Time": timeMain[0]
        }
        csv_writer.writerow(info)
    count += 1
    if count == 2:
        compute_threshold_ranges(window1Frequency, window1Time)
        count = 0
        window1Frequency = []
        window1Time = []
    time.sleep(1)


# # plotting code
# plt.xlabel("Time", fontsize=2)
# plt.ylabel("Distraction Level")
# plt.xticks(rotation=90)
# plt.plot(window1Time, window1Frequency)
# # f_smoothed = signal.savgol_filter(window2Frequency, 12, 3)
# # freqs = fft.rfft(f_smoothed)
# # freqs = freqs*numpy.array(list([int(x < 7)
# #                           for x in range(len(freqs))]), dtype=numpy.int32)
# # freqs = fft.irfft(freqs)
# # x_vals = list([x for x in range(len(freqs))])
# # f_cubic = interpolate.CubicSpline(x_vals[::10], freqs[::10])
# # f_cubic = numpy.vectorize(f_cubic)
# # # plt.plot(window2Time, f_smoothed, color='red')
# # # plt.plot(window2Time, f_cubic(x_vals), color='red')
# # smoooooth = numpy.linspace(min(x_vals), max(x_vals), 5000)
# # plt.plot(smoooooth, f_cubic(smoooooth))

# plt.show()
