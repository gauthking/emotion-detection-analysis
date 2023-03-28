import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd

x = []
y = []


def animate(i):
    dat = pd.read_csv(
        "D:\\VIT\\Sensors Project\\emotion-detection-analysis\\freqvtimew1.csv")
    x = dat['Time']
    y = dat['DistressFreq']
    print(x, y)
    plt.cla()
    plt.plot(x, y)


ani = animation.FuncAnimation(plt.gcf(), animate, interval=100)

plt.show()
