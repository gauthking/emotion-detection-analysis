from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation


x = []
y = []
df = pd.read_csv(
    r"D:\\MainFolders\\VIT\ACADEMICYEAR\\secondYEAR\\fourthsem\\sensors-da\\emotion-detection\\Emotion_detection_with_CNN\\plot4.csv")
counter = count(0, 1)
fig, ax = plt.subplots()
ax.plot(x, y)


def update(i):
    idx = next(counter)
    y.append(df.iloc[idx, 0])
    x.append(df.iloc[idx, 1])
    plt.cla()


ani = animation.FuncAnimation(
    fig=fig, func=update, interval=3000, cache_frame_data=False)
plt.show()
