import dearpygui
import numpy as np
import pandas as pd

s= range(0,13)
s = list(s)
# for i in range(35000,37000,500):
df = pd.read_csv("TO_Shootout_Lap.csv",sep=",",skiprows=[16,17],encoding='unicode_escape',header=14)

# print(i)
