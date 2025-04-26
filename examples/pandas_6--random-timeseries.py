import random
import pandas as pd

index = pd.date_range("2024-01-01 00:00", "2024-01-02 23:59", freq="min")
data = [random.uniform(0, 1) * 10 for _ in index]
time_ser = pd.Series(data=data, index=index)
print(time_ser)
time_ser.to_csv("non-real-data.csv", header=False)
