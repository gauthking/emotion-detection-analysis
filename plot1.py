import pandas as pd
import time
chunk = 20

for ch in pd.read_csv("plot3.csv", chunksize=chunk):
    print(list(ch['Time'])[0])

    time.sleep(5)
