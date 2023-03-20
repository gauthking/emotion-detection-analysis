import csv
from matplotlib import pyplot as plt
import time
import numpy
from scipy import signal, fft, interpolate

window1Frequency = []
window2Frequency = []

window1Time = []
window2Time = []

dcount = 0
ncount = 0

windowSize1 = 20
windowSize2 = 50

emotionsMain = []
timeMain = []


with open("plot2.csv", 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    plotData = list(plots)
    for row in plotData:
        if (row != []):
            emotionsMain.append(row[0])
            timeMain.append(row[1])
            if row[0] == "Distracted":
                dcount += 1
            else:
                ncount += 1
y = [dcount, ncount]
# print(emotionsMain)

for i in range(0, len(emotionsMain)-windowSize1):
    tempDict = {"tD": 0, "tN": 0}
    for j in range(i, i+windowSize1):
        if (emotionsMain[j] == "Distracted"):
            tempDict['tD'] += 1
        else:
            tempDict['tN'] += 1
    window1Frequency.append((tempDict['tD']/windowSize1)*100)
    window1Time.append((timeMain[i]))

    # if(tempDict['tD']>tempDict['tN']):
    #     print("Warning")
    #     break
    # else:
    #     continue


for i in range(0, len(emotionsMain)-windowSize2):
    tempDict = {"tD": 0, "tN": 0}

    for j in range(i, i+windowSize2):
        if (emotionsMain[j] == "Distracted"):
            tempDict['tD'] += 1
        else:
            tempDict['tN'] += 1
    window2Frequency.append((tempDict['tD']/windowSize2) * 100)
    window2Time.append((timeMain[i]))

    # if(tempDict['tD']>tempDict['tN']):
    #     if((tempDict['tD']/(tempDict['tD']+tempDict['tN'])) > 0.8):
    #         print("Stop the Car now! Calling emergency services")
    #         break
    #     elif((tempDict['tD']/(tempDict['tD']+tempDict['tN']))<0.8 and (tempDict['tD']/(tempDict['tD']+tempDict['tN']))>0.45):
    #         print("Distraction levels between 45-80 percent Should I call the emergency services")
    #         break

    # elif(tempDict['tN']>tempDict['tD']):
    #     if((tempDict['tD']/(tempDict['tD']+tempDict['tN']))>0.3):
    #         print("Distraction levels are increasing.. concentrate on the road")
    #         continue

# print(window1Frequency)
# print(window2Frequency)

print(window2Frequency)

thresholdAboveCount = 0

# for i in range(0, len(window1Frequency)-(len(window1Frequency)/3)):
#     for j in range(i, i+(len(window1Frequency)/3)):
#         if(window1Frequency[j]>76.0):
#             thresholdAboveCount+=1

print(thresholdAboveCount/len(window1Frequency))


plt.xlabel("Time", fontsize=2)
plt.ylabel("Distraction Level")
plt.xticks(rotation=90)
# f_gradient = numpy.gradient(window2Frequency)
f_smoothed = signal.savgol_filter(window2Frequency, 12, 3)
freqs = fft.rfft(f_smoothed)
freqs = freqs*numpy.array(list([int(x < 7)
                          for x in range(len(freqs))]), dtype=numpy.int32)
freqs = fft.irfft(freqs)
x_vals = list([x for x in range(len(freqs))])
f_cubic = interpolate.CubicSpline(x_vals[::10], freqs[::10])
f_cubic = numpy.vectorize(f_cubic)
# plt.plot(window2Time, f_smoothed, color='red')
# plt.plot(window2Time, f_cubic(x_vals), color='red')
smoooooth = numpy.linspace(min(x_vals), max(x_vals), 5000)
plt.plot(smoooooth, f_cubic(smoooooth))
plt.show()
