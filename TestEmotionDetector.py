import cv2
import numpy as np
from keras.models import model_from_json
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import winsound


beepFreq = 1500
duration = 1400


emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# load json and create model
json_file = open('./model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("./model/emotion_model.h5")
print("Loaded model from disk")

# start the webcam feed
# cap = cv2.VideoCapture(0)

# pass here your video path
# you may download one from here : https://www.pexels.com/video/three-girls-laughing-5273028/
cap = cv2.VideoCapture(0)

colNames = ["Mood", "Time"]
with open("plot3.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=colNames)
    csv_writer.writeheader()

fields1 = ["DistressFreq", "Time"]
with open("freqvtimew1.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields1)
    csv_writer.writeheader()

fields2 = ["starttime", "endtime", "seconds"]
with open("distressRanges.csv", 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fields2)
    csv_writer.writeheader()


windowSize = 10

start = ''
j = 0


def compute_threshold_ranges(freqRange, ti):
    global start, j
    levelsCount = 0
    for i in range(len(freqRange)):
        if (freqRange[i] > 75):
            if j == 0:
                start = ti[i]
                print(start)
            j += 1
        elif (freqRange[i] < 75 and start != ''):
            levelsCount += 1
            print(
                f"Distraction level - {levelsCount} start time - {start} end time - {str(ti[i])}. Estimated duration of distraction - ", datetime.strptime(str(ti[i]), "%H:%M:%S") - datetime.strptime(start, "%H:%M:%S"))
            winsound.Beep(beepFreq, duration)
            est = datetime.strptime(
                str(ti[i]), "%H:%M:%S") - datetime.strptime(start, "%H:%M:%S")
            with open("distressRanges.csv", 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fields2)
                info = {
                    "starttime": start,
                    "endtime": str(ti[i]),
                    "seconds": est
                }
                csv_writer.writerow(info)
            j = 0
            start = ''


def write_into_csv(fields):
    with open("plot3.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=colNames)
        info = {
            "Mood": fields[0],
            "Time": fields[1]
        }
        csv_writer.writerow(info)


countCall = 0
tempEmot = []
tempTime = []

rangeCount = 0
rangeFreq = []
rangeTime = []

while True:
    # Find haar cascade to draw bounding box around face
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break
    face_detector = cv2.CascadeClassifier(
        './haarcascades/haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces available on camera
    num_faces = face_detector.detectMultiScale(
        gray_frame, scaleFactor=1.3, minNeighbors=5)

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(
            cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        if (emotion_dict[maxindex] == "Angry" or emotion_dict[maxindex] == "Disgusted" or emotion_dict[maxindex] == "Fearful" or emotion_dict[maxindex] == "Surprised"):
            ti = datetime.now().strftime("%H:%M:%S")
            fields = ["Distracted",
                      ti]
            write_into_csv(fields)
            countCall += 1
            tempEmot.append("Distracted")
            tempTime.append(ti)
        elif (emotion_dict[maxindex] != "Angry" or emotion_dict[maxindex] != "Disgusted" or emotion_dict[maxindex] != "Fearful" or emotion_dict[maxindex] != "Surprised"):
            ti = datetime.now().strftime("%H:%M:%S")
            fields = ["Neutral", ti]
            write_into_csv(fields)
            countCall += 1
            tempEmot.append("Neutral")
            tempTime.append(ti)
        else:
            ti = datetime.now().strftime("%H:%M:%S")
            fields = ["Neutral", ti]
            write_into_csv(fields)
            countCall += 1
            tempEmot.append("Neutral")
            tempTime.append(ti)
        if (countCall % windowSize == 0):
            tempDict = {"tD": 0, "tN": 0}
            for i in range(len(tempEmot)):
                if (tempEmot[i] == "Distracted"):
                    tempDict["tD"] += 1
                elif (tempEmot[i] == "Neutral"):
                    tempDict["tN"] += 1
            with open("freqvtimew1.csv", 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fields1)
                info = {
                    "DistressFreq": (tempDict['tD']/windowSize)*100,
                    "Time": tempTime[0]
                }
                csv_writer.writerow(info)
            rangeCount += 1
            rangeFreq.append((tempDict['tD']/windowSize)*100)
            rangeTime.append(tempTime[0])
            tempTime = []
            tempEmot = []

        if (rangeCount == 7):
            compute_threshold_ranges(rangeFreq, rangeTime)
            rangeCount = 0
            rangeFreq = []
            rangeTime = []

    cv2.imshow('Emotion Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
